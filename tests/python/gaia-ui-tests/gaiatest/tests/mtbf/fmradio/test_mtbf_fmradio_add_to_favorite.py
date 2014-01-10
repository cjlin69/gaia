# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.fmradio.app import FmRadio
import time


class TestFMRadioAddToFavorite(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)

        # launch the FM Radio app
        self.fm_radio = FmRadio(self.marionette)
        self.app_id = self.launch_by_touch("FM Radio")
        time.sleep(5)

    def test_add_to_favorite(self):
        """ Add a frequency to favorite list

        https://moztrap.mozilla.org/manage/case/1923/

        """
        # check the headphone is plugged-in or not
        self.assertTrue(self.data_layer.is_antenna_available, 'Antenna (headphones) not plugged in')

        # if power button is not on, turn it on
        if not self.fm_radio.is_power_button_on:
            self.fm_radio.tap_power_button()

        # wait for the radio start-up
        self.wait_for_condition(lambda m: self.data_layer.is_fm_radio_enabled)

        # add the current frequency to favorite list
        self.fm_radio.tap_add_favorite()

        self.assertEqual(len(self.fm_radio.favorite_channels), 1)

        # verify that the current frequency is in the favorite frequency is equal to the
        self.assertEqual(self.fm_radio.frequency, self.fm_radio.favorite_channels[0].text)

    def tearDown(self):
        # remove the station from favorite list
        for favorite_channel in self.fm_radio.favorite_channels:
            favorite_channel.remove()

        GaiaMtbfTestCase.tearDown(self)
