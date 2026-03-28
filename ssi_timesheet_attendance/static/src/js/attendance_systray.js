// Copyright 2022 OpenSynergy Indonesia
// Copyright 2022 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
odoo.define("ssi_timesheet_attendance.AttendanceSystray", function (require) {
    "use strict";

    var SystrayMenu = require("web.SystrayMenu");
    var Widget = require("web.Widget");
    var session = require("web.session");

    var AttendanceSystray = Widget.extend({
        template: "ssi_timesheet_attendance.AttendanceSystray",
        sequence: 50,

        events: {
            "click .o_attendance_sign_in": "_onSignIn",
            "click .o_attendance_sign_out": "_onSignOut",
        },

        init: function () {
            this._super.apply(this, arguments);
            this._employeeId = false;
            this._attendanceStatus = false;
        },

        willStart: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                return self._fetchStatus();
            });
        },

        start: function () {
            this._super.apply(this, arguments);
            this._updateButtons();
        },

        _fetchStatus: function () {
            var self = this;
            return this._rpc({
                model: "hr.employee",
                method: "search_read",
                args: [[["user_id", "=", session.uid]]],
                kwargs: {
                    fields: ["id", "attendance_status"],
                    limit: 1,
                },
            }).then(function (result) {
                if (result.length > 0) {
                    self._employeeId = result[0].id;
                    self._attendanceStatus = result[0].attendance_status;
                }
            });
        },

        _updateButtons: function () {
            var hasEmployee = Boolean(this._employeeId);
            this.$el.toggleClass("d-none", !hasEmployee);
            if (!hasEmployee) {
                return;
            }
            this.$(".o_attendance_sign_in").toggleClass(
                "d-none",
                this._attendanceStatus === "sign_in"
            );
            this.$(".o_attendance_sign_out").toggleClass(
                "d-none",
                this._attendanceStatus === "sign_out"
            );
        },

        _onSignIn: function (ev) {
            ev.preventDefault();
            var self = this;
            if (!this._employeeId) {
                return;
            }
            this._rpc({
                model: "hr.employee",
                method: "action_sign_in",
                args: [[this._employeeId]],
            }).then(function () {
                self._attendanceStatus = "sign_in";
                self._updateButtons();
            });
        },

        _onSignOut: function (ev) {
            ev.preventDefault();
            var self = this;
            if (!this._employeeId) {
                return;
            }
            this._rpc({
                model: "hr.employee",
                method: "action_sign_out",
                args: [[this._employeeId]],
            }).then(function () {
                self._attendanceStatus = "sign_out";
                self._updateButtons();
            });
        },
    });

    SystrayMenu.Items.push(AttendanceSystray);

    return AttendanceSystray;
});
