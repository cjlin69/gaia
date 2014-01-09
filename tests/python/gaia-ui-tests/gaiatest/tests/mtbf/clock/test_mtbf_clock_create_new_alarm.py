# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.clock.app import Clock
import time


class TestClockCreateNewAlarm(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)

        self.clock = Clock(self.marionette)
        self.app_id = self.launch_by_touch("Clock")
        time.sleep(5)

        if len(self.marionette.find_elements('id', 'alarm-close')) > 0:
            if self.marionette.find_element('id', 'alarm-close').is_displayed():
                self.marionette.find_element('id', 'alarm-close').tap()
        if len(self.marionette.find_elements('id', 'alarm-tab')) > 0:
            self.wait_for_element_displayed('id', 'alarm-tab')
            self.marionette.find_element('id', 'alarm-tab').tap()

    def test_clock_create_new_alarm(self):
        """ Add an alarm and set label of the new alarm
        https://moztrap.mozilla.org/manage/case/1772/
        https://moztrap.mozilla.org/manage/case/1775/
        """

        alarm_label_text = "test4321"

        # get the number of alarms set, before adding the new alarm
        initial_alarms_count = len(self.clock.alarms)

        # create a new alarm with the default values that are available
        new_alarm = self.clock.tap_new_alarm()

        # set label
        new_alarm.type_alarm_label(alarm_label_text)
        self.clock = new_alarm.tap_done()

        # verify the banner-countdown message appears
        alarm_msg = self.clock.banner_countdown_notification
        self.assertTrue('The alarm is set for' in alarm_msg, 'Actual banner message was: "' + alarm_msg + '"')

        # ensure the new alarm has been added and is displayed
        self.assertTrue(initial_alarms_count < len(self.clock.alarms),
                        'Alarms count did not increment')

        # verify the label of alarm
        self.clock.wait_for_banner_not_visible()
        alarms = self.clock.alarms
        self.assertEqual(len(alarms), initial_alarms_count + 1)
        self.assertEqual(alarms[0].label, alarm_label_text)
