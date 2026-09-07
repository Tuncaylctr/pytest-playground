import logging
from datetime import datetime
from decimal import Decimal

import pytest

from pftracker import JsonFileStorage, PersonalFinanceTracker, UnknownCategory, UnknownTransaction



class TestConversions:
    @pytest.fixture(scope="class")
    def mock_conversion_rate(self, class_mocker):
        def _get_conversion_rate(*args, **kwargs):
            return Decimal("0.9")

        return class_mocker.patch(
            "pftracker.main.PersonalFinanceTracker._get_conversion_rate",
            # return_value=Decimal("0.9"),
            side_effect=_get_conversion_rate,
        )

    def test_transactions_in_different_currency(
        self, tracker, mock_conversion_rate, mocker
    ):
        convert_tracker = mocker.spy(PersonalFinanceTracker, "_convert")
        tracker.add_transaction(when="2020-01-05", amount=Decimal("100"), currency="USD")
        assert tracker.balance() == Decimal("90")

        mock_conversion_rate.assert_called_once()
        assert mock_conversion_rate.call_count == 1
        # mock_conversion_rate.call_args_list

        convert_tracker.assert_called_once()
        # convert_tracker.call_args_list

    def test_transactions_in_different_currency_v2(self, tmp_path, mocker):
        # autospec is used for not having mock drift.
        MockECBRateProvider = mocker.patch("pftracker.main.ECBRateProvider", autospec=True)
        print(MockECBRateProvider)

        MockECBRateProvider.return_value.get_rate.return_value = Decimal("0.9")

        json_storage_path = tmp_path / "finance.json"
        storage = JsonFileStorage(json_storage_path)

        with PersonalFinanceTracker(storage) as t:
            t.add_transaction(when="2020-01-05", amount=Decimal("100"), currency="USD")
            assert t.balance() == Decimal("90")

        MockECBRateProvider.return_value.get_rate.assert_called_once()
