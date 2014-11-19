"""
Contains form class definitions.
"""
from django import forms
from django.utils.translation import ugettext as _


COUNTRIES = (
    (286, _(u'Aaland Islands')),
    (274, _(u'Afghanistan')),
    (2, _(u'Albania')),
    (3, _(u'Algeria')),
    (178, _(u'American Samoa')),
    (4, _(u'Andorra')),
    (5, _(u'Angola')),
    (176, _(u'Anguilla')),
    (175, _(u'Antigua And Barbuda')),
    (6, _(u'Argentina')),
    (7, _(u'Armenia')),
    (179, _(u'Aruba')),
    (8, _(u'Australia')),
    (9, _(u'Austria')),
    (10, _(u'Azerbaijan')),
    (11, _(u'Bahamas')),
    (12, _(u'Bahrain')),
    (13, _(u'Bangladesh')),
    (14, _(u'Barbados')),
    (15, _(u'Belarus')),
    (16, _(u'Belgium')),
    (17, _(u'Belize')),
    (18, _(u'Benin')),
    (19, _(u'Bermuda')),
    (20, _(u'Bhutan')),
    (21, _(u'Bolivia')),
    (22, _(u'Bosnia and Herzegovina')),
    (23, _(u'Botswana')),
    (181, _(u'Bouvet Island')),
    (24, _(u'Brazil')),
    (180, _(u'Brunei Darussalam')),
    (25, _(u'Bulgaria')),
    (26, _(u'Burkina Faso')),
    (27, _(u'Burundi')),
    (28, _(u'Cambodia')),
    (29, _(u'Cameroon')),
    (30, _(u'Canada')),
    (31, _(u'Cape Verde')),
    (32, _(u'Cayman Islands')),
    (33, _(u'Central African Republic')),
    (34, _(u'Chad')),
    (35, _(u'Chile')),
    (36, _(u'China')),
    (185, _(u'Christmas Island')),
    (37, _(u'Colombia')),
    (204, _(u'Comoros')),
    (38, _(u'Congo')),
    (183, _(u'Cook Islands')),
    (268, _(u'Costa Rica')),
    (275, _(u'Cote D\'Ivoire')),
    (40, _(u'Croatia')),
    (276, _(u'Cuba')),
    (298, _(u'Curacao')),
    (41, _(u'Cyprus')),
    (42, _(u'Czech Republic')),
    (318, _(u'Democratic Republic of the Congo')),
    (43, _(u'Denmark')),
    (44, _(u'Djibouti')),
    (186, _(u'Dominica')),
    (289, _(u'Dominica')),
    (187, _(u'Dominican Republic')),
    (45, _(u'Ecuador')),
    (46, _(u'Egypt')),
    (47, _(u'El Salvador')),
    (48, _(u'Equatorial Guinea')),
    (49, _(u'Eritrea')),
    (50, _(u'Estonia')),
    (51, _(u'Ethiopia')),
    (189, _(u'Falkland Islands')),
    (191, _(u'Faroe Islands')),
    (52, _(u'Fiji')),
    (53, _(u'Finland')),
    (54, _(u'France')),
    (193, _(u'French Guiana')),
    (277, _(u'French Polynesia')),
    (56, _(u'Gabon')),
    (57, _(u'Gambia')),
    (58, _(u'Georgia')),
    (59, _(u'Germany')),
    (60, _(u'Ghana')),
    (194, _(u'Gibraltar')),
    (61, _(u'Greece')),
    (195, _(u'Greenland')),
    (192, _(u'Grenada')),
    (196, _(u'Guadeloupe')),
    (62, _(u'Guam')),
    (198, _(u'Guatemala')),
    (270, _(u'Guernsey')),
    (63, _(u'Guinea')),
    (65, _(u'Guyana')),
    (200, _(u'Haiti')),
    (66, _(u'Honduras')),
    (67, _(u'Hong Kong')),
    (68, _(u'Hungary')),
    (69, _(u'Iceland')),
    (70, _(u'India')),
    (71, _(u'Indonesia')),
    (278, _(u'Iran')),
    (279, _(u'Iraq')),
    (74, _(u'Ireland')),
    (322, _(u'Isle of Man')),
    (75, _(u'Israel')),
    (76, _(u'Italy')),
    (202, _(u'Jamaica')),
    (78, _(u'Japan')),
    (288, _(u'Jersey  (Channel Islands)')),
    (79, _(u'Jordan')),
    (80, _(u'Kazakhstan')),
    (81, _(u'Kenya')),
    (203, _(u'Kiribati')),
    (82, _(u'Kuwait')),
    (83, _(u'Kyrgyzstan')),
    (84, _(u'Lao People\'s Democratic Republic')),
    (85, _(u'Latvia')),
    (86, _(u'Lebanon')),
    (87, _(u'Lesotho')),
    (88, _(u'Liberia')),
    (281, _(u'Libya')),
    (90, _(u'Liechtenstein')),
    (91, _(u'Lithuania')),
    (92, _(u'Luxembourg')),
    (208, _(u'Macau')),
    (93, _(u'Macedonia')),
    (94, _(u'Madagascar')),
    (95, _(u'Malawi')),
    (96, _(u'Malaysia')),
    (97, _(u'Maldives')),
    (98, _(u'Mali')),
    (99, _(u'Malta')),
    (207, _(u'Marshall Islands')),
    (210, _(u'Martinique')),
    (100, _(u'Mauritania')),
    (212, _(u'Mauritius')),
    (241, _(u'Mayotte')),
    (101, _(u'Mexico')),
    (102, _(u'Moldova, Republic of')),
    (103, _(u'Monaco')),
    (104, _(u'Mongolia')),
    (290, _(u'Montenegro')),
    (294, _(u'Montserrat')),
    (105, _(u'Morocco')),
    (106, _(u'Mozambique')),
    (242, _(u'Myanmar')),
    (107, _(u'Namibia')),
    (108, _(u'Nepal')),
    (109, _(u'Netherlands')),
    (110, _(u'Netherlands Antilles')),
    (213, _(u'New Caledonia')),
    (111, _(u'New Zealand')),
    (112, _(u'Nicaragua')),
    (113, _(u'Niger')),
    (114, _(u'Nigeria')),
    (217, _(u'Niue')),
    (214, _(u'Norfolk Island')),
    (272, _(u'North Korea')),
    (116, _(u'Norway')),
    (117, _(u'Oman')),
    (118, _(u'Pakistan')),
    (222, _(u'Palau')),
    (282, _(u'Palestine')),
    (119, _(u'Panama')),
    (219, _(u'Papua New Guinea')),
    (120, _(u'Paraguay')),
    (121, _(u'Peru')),
    (122, _(u'Philippines')),
    (221, _(u'Pitcairn')),
    (123, _(u'Poland')),
    (124, _(u'Portugal')),
    (253, _(u'Puerto Rico')),
    (126, _(u'Qatar')),
    (315, _(u'Republic of Kosovo')),
    (127, _(u'Reunion')),
    (128, _(u'Romania')),
    (129, _(u'Russia')),
    (130, _(u'Rwanda')),
    (205, _(u'Saint Kitts and Nevis')),
    (206, _(u'Saint Lucia')),
    (237, _(u'Saint Vincent and the Grenadines')),
    (132, _(u'Samoa (Independent)')),
    (227, _(u'San Marino')),
    (255, _(u'Sao Tome and Principe')),
    (133, _(u'Saudi Arabia')),
    (134, _(u'Senegal')),
    (266, _(u'Serbia')),
    (135, _(u'Seychelles')),
    (136, _(u'Sierra Leone')),
    (137, _(u'Singapore')),
    (302, _(u'Sint Maarten')),
    (138, _(u'Slovakia')),
    (139, _(u'Slovenia')),
    (223, _(u'Solomon Islands')),
    (140, _(u'Somalia')),
    (141, _(u'South Africa')),
    (257, _(u'South Georgia and the South Sandwich Islands')),
    (142, _(u'South Korea')),
    (311, _(u'South Sudan')),
    (143, _(u'Spain')),
    (144, _(u'Sri Lanka')),
    (293, _(u'Sudan')),
    (146, _(u'Suriname')),
    (225, _(u'Svalbard and Jan Mayen Islands')),
    (147, _(u'Swaziland')),
    (148, _(u'Sweden')),
    (149, _(u'Switzerland')),
    (285, _(u'Syria')),
    (152, _(u'Taiwan')),
    (260, _(u'Tajikistan')),
    (153, _(u'Tanzania')),
    (154, _(u'Thailand')),
    (233, _(u'Timor-Leste')),
    (155, _(u'Togo')),
    (232, _(u'Tonga')),
    (234, _(u'Trinidad and Tobago')),
    (156, _(u'Tunisia')),
    (157, _(u'Turkey')),
    (287, _(u'Turks & Caicos Islands')),
    (159, _(u'Uganda')),
    (161, _(u'Ukraine')),
    (162, _(u'United Arab Emirates')),
    (262, _(u'United Kingdom')),
    (164, _(u'United States')),
    (163, _(u'Uruguay')),
    (165, _(u'Uzbekistan')),
    (239, _(u'Vanuatu')),
    (166, _(u'Vatican City State (Holy See)')),
    (167, _(u'Venezuela')),
    (168, _(u'Vietnam')),
    (169, _(u'Virgin Islands (British)')),
    (238, _(u'Virgin Islands (U.S.)')),
    (188, _(u'Western Sahara')),
    (170, _(u'Yemen')),
    (173, _(u'Zambia')),
    (174, _(u'Zimbabwe')),
)

class CountryField(forms.ChoiceField):
    """
    Renders a select element populated with world countries.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the instance.
        """
        kwargs.setdefault('choices', COUNTRIES)
        super(CountryField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        """
        Returns internal class type.

        :rtype: str.
        """
        return 'ChoiceField'
