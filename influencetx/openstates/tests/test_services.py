from datetime import timedelta
from unittest import mock

from django.test import TestCase

from influencetx.bills.factories import BillFactory
from influencetx.legislators import factories
from influencetx.openstates import data, services, utils
from influencetx.openstates.factories import fake_bill_detail, fake_openstates_timestamp
from influencetx.openstates.testing import assert_legislator_fields_match_data


ONE_DAY = timedelta(days=1)


def test_sync_new_legislator_data():
    api_data = data.get_sample_legislator_detail()
    info = services.sync_new_legislator_data(api_data, commit=False)

    assert info.action == services.Action.ADDED
    assert_legislator_fields_match_data(info.instance, api_data)


def test_sync_new_legislator_with_data_with_missing_keys_fails():
    bad_data_input = {}
    info = services.sync_new_legislator_data(bad_data_input, commit=False)
    assert info.action == services.Action.FAILED
    assert 'missing key' in info.error


def test_sync_new_legislator_without_leg_id_fails():
    data_with_invalid_id = data.get_sample_legislator_detail()
    data_with_invalid_id['leg_id'] = ''  # 'leg_id' is a required field.
    info = services.sync_new_legislator_data(data_with_invalid_id, commit=False)

    assert info.action == services.Action.FAILED
    assert 'openstates_leg_id' in info.error


def test_sync_existing_legislator_data_updates_from_recently_updated_data():
    instance = factories.LegislatorFactory.build()
    original_id = instance.id
    updated_at = utils.format_datetime(instance.openstates_updated_at + ONE_DAY)
    api_data = data.get_sample_legislator_detail(updated_at=updated_at)

    info = services.sync_existing_legislator_data(instance, api_data, commit=False)

    assert info.action == services.Action.UPDATED
    assert_legislator_fields_match_data(info.instance, api_data)
    assert info.instance.id == original_id


def test_sync_existing_legislator_data_skips_old_data():
    instance = factories.LegislatorFactory.build()
    original_id = instance.id
    updated_at = utils.format_datetime(instance.openstates_updated_at - ONE_DAY)
    api_data = data.get_sample_legislator_detail(updated_at=updated_at)

    info = services.sync_existing_legislator_data(instance, api_data, commit=False)

    assert info.action == services.Action.SKIPPED
    assert info.instance.id == original_id


class TestSyncLegislatorData(TestCase):

    @mock.patch.object(services, 'sync_existing_legislator_data')
    def test_sync_legislator_data_for_existing_data(self, mock_sync_existing):
        instance = factories.LegislatorFactory.create()
        data = {'leg_id': instance.openstates_leg_id}
        services.sync_legislator_data(data)
        mock_sync_existing.assert_called_once_with(instance, data, commit=True)

    @mock.patch.object(services, 'sync_new_legislator_data')
    def test_sync_legislator_data_for_new_data(self, mock_sync_new):
        data = {'leg_id': 'TX00001'}
        services.sync_legislator_data(data)
        mock_sync_new.assert_called_once_with(data, commit=True)


class TestSyncBillData(TestCase):

    def test_sync_new_bill(self):
        new_data = {'id': 'BILL0001', 'updated_at': fake_openstates_timestamp()}

        with mock.patch.object(utils, 'deserialize_openstates_bill') as mock_deserialize:
            info = services.sync_bill_data(new_data)

        mock_deserialize.assert_called_once_with(new_data)
        assert info.action == services.Action.ADDED

    def test_sync_bill_with_long_bill_id(self):
        bad_data = fake_bill_detail()
        bad_data['id'] = 'X' * 100

        info = services.sync_bill_data(bad_data)
        assert info.action == services.Action.FAILED

    def test_sync_existing_bill_updates_given_newer_data(self):
        instance = BillFactory.create()
        newer_data = {
            'id': instance.openstates_bill_id,
            'updated_at': utils.format_datetime(instance.openstates_updated_at + ONE_DAY),
        }

        with mock.patch.object(utils, 'deserialize_openstates_bill') as mock_deserialize:
            info = services.sync_bill_data(newer_data)

        mock_deserialize.assert_called_once_with(newer_data, instance=instance)
        assert info.action == services.Action.UPDATED

    def test_sync_existing_bill_skips_older(self):
        instance = BillFactory.create()
        older_data = {
            'id': instance.openstates_bill_id,
            'updated_at': utils.format_datetime(instance.openstates_updated_at - ONE_DAY),
        }

        with mock.patch.object(utils, 'deserialize_openstates_bill') as mock_deserialize:
            info = services.sync_bill_data(older_data)

        mock_deserialize.assert_not_called()
        assert info.action == services.Action.SKIPPED
