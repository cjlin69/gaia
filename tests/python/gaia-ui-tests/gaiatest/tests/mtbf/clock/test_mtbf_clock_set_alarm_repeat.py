# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.clock.app import Clock
import time


class TestClockSetAlarmRepeat(GaiaMtbfTestCase):

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

    def test_clock_set_alarm_repeat(self):
        """ Modify the alarm repeat

        https://moztrap.mozilla.org/manage/case/1786/
        Test that [Clock][Alarm] Change the repeat state

        """
        new_alarm = self.clock.tap_new_alarm()

        # Set label
        new_alarm.type_alarm_label("TestSetAlarmRepeat")

        # loop the options and select the ones in match list
        for option in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            new_alarm.select_repeat(option)

        self.assertEqual('Weekdays', new_alarm.alarm_repeat)

        # check select Sunday twice
        new_alarm.select_repeat('Sunday')
        self.assertEqual('Mon, Tue, Wed, Thu, Fri, Sun', new_alarm.alarm_repeat)

        new_alarm.select_repeat('Sunday')
        self.assertEqual('Weekdays', new_alarm.alarm_repeat)

        # Save the alarm
        new_alarm.tap_done()
        self.clock.wait_for_banner_not_visible()

        # Tap to Edit alarm
        edit_alarm = self.clock.alarms[0].tap()

        # To verify the select list.
        self.assertEqual('Weekdays', edit_alarm.alarm_repeat)

        # Close alarm
        edit_alarm.tap_done()
        self.clock.wait_for_banner_not_visible()

