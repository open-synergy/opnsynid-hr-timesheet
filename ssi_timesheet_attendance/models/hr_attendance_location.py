# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrAttendanceLocation(models.Model):
    """Registered attendance location, with a center point and radius.

    An organization registers the physical places where attendance is
    officially allowed to be taken (e.g. "Head Office", "Branch A"),
    each with a coordinate pair and a tolerance radius in meters. This
    master data does not, by itself, restrict where an attendance
    record can be taken - it only names and stores the geolocation
    values that other models compare against.
    """

    _name = "hr.attendance_location"
    _inherit = ["mixin.master_data"]
    _description = "Attendance Location"

    name = fields.Char(
        string="Location",
    )
    latitude = fields.Float(
        string="Latitude",
        digits=(16, 7),
        required=True,
        help="Latitude of the location's center point, in decimal "
        "degrees (-90 to 90). Stored with 7 decimal digits of "
        "precision (~1 cm) so the tolerance radius stays meaningful.",
    )
    longitude = fields.Float(
        string="Longitude",
        digits=(16, 7),
        required=True,
        help="Longitude of the location's center point, in decimal "
        "degrees (-180 to 180). Stored with 7 decimal digits of "
        "precision (~1 cm) so the tolerance radius stays meaningful.",
    )
    radius = fields.Float(
        string="Radius (meter)",
        digits=(16, 2),
        required=True,
        default=100.0,
        help="Tolerance radius around the center point, in METERS. "
        "An attendance reading within this distance of the center "
        "point is considered to be taken at this location.",
    )

    @api.constrains("latitude", "longitude", "radius")
    def _check_location_coordinate(self):
        """Validate the center point and radius of the location.

        Unlike device-captured geolocation on an attendance record,
        this coordinate is deliberately typed in by a configurator, so
        an all-zero pair is a data entry mistake rather than a
        legitimate "no reading" value and is rejected here.

        :raises ValidationError: if latitude is outside ``-90..90``,
            longitude is outside ``-180..180``, ``radius`` is zero or
            negative, or latitude and longitude are both exactly
            ``0.0``.
        """
        for record in self:
            if record.latitude < -90.0 or record.latitude > 90.0:
                raise ValidationError(_("Latitude must be between -90 and 90 degrees."))
            if record.longitude < -180.0 or record.longitude > 180.0:
                raise ValidationError(
                    _("Longitude must be between -180 and 180 degrees.")
                )
            if record.radius <= 0.0:
                raise ValidationError(_("Radius must be greater than 0."))
            if record.latitude == 0.0 and record.longitude == 0.0:
                raise ValidationError(
                    _(
                        "Latitude and longitude cannot both be 0. "
                        "Enter the actual coordinate of the location."
                    )
                )
