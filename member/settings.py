# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

COUNTRY_CHOICES = (
    (0, _('Taiwan')),
    (1, _('China')),
)

GENDER_CHOICES = (
    (0, _('Male')),
    (1, _('Female')),
)

RESERVED_KEYWORD = ('empor', 'EMPOR', 'EMPOR-TW', 'empor-tw')

CITY_CHOICES =(
    (1, ('台北市')),
    (2, ('新北市')),
    (3, ('基隆市')),
    (4, ('桃園縣')),
    (5, ('新竹縣')),
    (6, ('新竹市')),
    (7, ('台中市')),
    (9, ('苗栗縣')),
    (10, ('彰化縣')),
    (11, ('雲林縣')),
    (12, ('南投縣')),
    (13, ('嘉義市')),
    (14, ('嘉義縣')),
    (15, ('台南市')),
    (16, ('高雄市')),
    (8, ('宜蘭縣')),
    (19, ('花蓮縣')),
    (18, ('台東縣')),
    (17, ('澎湖縣')),
    (20, ('金門縣')),
    (21, ('連江縣')),
)

AREA_CHOICES = (
    (100, ('中正區 100')),
    (103, ('大同區 103')),
    (104, ('中山區 104')),
    (105, ('松山區 105')),
    (106, ('大安區 106')),
    (108, ('萬華區 108')),
    (110, ('信義區 110')),
    (111, ('士林區 111')),
    (112, ('北投區 112')),
    (114, ('內湖區 114')),
    (115, ('南港區 115')),
    (116, ('文山區 116')),
    (817, ('東　沙 817')),
    (819, ('南　沙 819')),
    (290, ('釣魚台 290')),
    (200, ('仁愛區 200')),
    (201, ('信義區 201')),
    (202, ('中正區 202')),
    (203, ('中山區 203')),
    (204, ('安樂區 204')),
    (205, ('暖暖區 205')),
    (206, ('七堵區 206')),
    (207, ('萬里區 207')),
    (208, ('金山區 208')),
    (220, ('板橋區 220')),
    (221, ('汐止區 221')),
    (222, ('深坑區 222')),
    (223, ('石碇區 223')),
    (224, ('瑞芳區 224')),
    (226, ('平溪區 226')),
    (227, ('雙溪區 227')),
    (228, ('貢寮區 228')),
    (231, ('新店區 231')),
    (232, ('坪林區 232')),
    (233, ('烏來區 233')),
    (234, ('永和區 234')),
    (235, ('中和區 235')),
    (236, ('土城區 236')),
    (237, ('三峽區 237')),
    (238, ('樹林區 238')),
    (239, ('鶯歌區 239')),
    (241, ('三重區 241')),
    (242, ('新莊區 242')),
    (243, ('泰山區 243')),
    (244, ('林口區 244')),
    (247, ('蘆洲區 247')),
    (248, ('五股區 248')),
    (249, ('八里區 249')),
    (251, ('淡水區 251')),
    (252, ('三芝區 252')),
    (253, ('石門區 253')),
    (260, ('宜蘭市 260')),
    (261, ('頭城鎮 261')),
    (262, ('礁溪鄉 262')),
    (263, ('壯圍鄉 263')),
    (264, ('員山鄉 264')),
    (265, ('羅東鎮 265')),
    (266, ('三星鄉 266')),
    (267, ('大同鄉 267')),
    (268, ('五結鄉 268')),
    (269, ('冬山鄉 269')),
    (270, ('蘇澳鎮 270')),
    (272, ('南澳鄉 272')),
    (209, ('南竿鄉 209')),
    (210, ('北竿鄉 210')),
    (211, ('莒光鄉 211')),
    (212, ('東引鄉 212')),
    (300, ('東　區 300')),
    (300, ('北　區 300')),
    (300, ('香山區 300')),
    (302, ('竹北市 302')),
    (303, ('湖口鄉 303')),
    (304, ('新豐鄉 304')),
    (305, ('新埔鎮 305')),
    (306, ('關西鎮 306')),
    (307, ('芎林鄉 307')),
    (308, ('寶山鄉 308')),
    (310, ('竹東鎮 310')),
    (311, ('五峰鄉 311')),
    (312, ('橫山鄉 312')),
    (313, ('尖石鄉 313')),
    (314, ('北埔鄉 314')),
    (315, ('峨眉鄉 315')),
    (320, ('中壢市 320')),
    (324, ('平鎮市 324')),
    (325, ('龍潭鄉 325')),
    (326, ('楊梅鎮 326')),
    (327, ('新屋鄉 327')),
    (328, ('觀音鄉 328')),
    (330, ('桃園市 330')),
    (333, ('龜山鄉 333')),
    (334, ('八德市 334')),
    (335, ('大溪鎮 335')),
    (336, ('復興鄉 336')),
    (337, ('大園鄉 337')),
    (338, ('蘆竹鄉 338')),
    (350, ('竹南鎮 350')),
    (351, ('頭份鎮 351')),
    (352, ('三灣鄉 352')),
    (353, ('南庄鄉 353')),
    (354, ('獅潭鄉 354')),
    (356, ('後龍鎮 356')),
    (357, ('通霄鎮 357')),
    (358, ('苑裡鎮 358')),
    (360, ('苗栗市 360')),
    (361, ('造橋鄉 361')),
    (362, ('頭屋鄉 362')),
    (363, ('公館鄉 363')),
    (364, ('大湖鄉 364')),
    (365, ('泰安鄉 365')),
    (366, ('銅鑼鄉 366')),
    (367, ('三義鄉 367')),
    (368, ('西湖鄉 368')),
    (369, ('卓蘭鎮 369')),
    (400, ('中　區 400')),
    (401, ('東　區 401')),
    (402, ('南　區 402')),
    (403, ('西　區 403')),
    (404, ('北　區 404')),
    (406, ('北屯區 406')),
    (407, ('西屯區 407')),
    (408, ('南屯區 408')),
    (411, ('太平區 411')),
    (412, ('大里區 412')),
    (413, ('霧峰區 413')),
    (414, ('烏日區 414')),
    (420, ('豐原區 420')),
    (421, ('后里區 421')),
    (422, ('石岡區 422')),
    (423, ('東勢區 423')),
    (424, ('和平區 424')),
    (426, ('新社區 426')),
    (427, ('潭子區 427')),
    (428, ('大雅區 428')),
    (429, ('神岡區 429')),
    (432, ('大肚區 432')),
    (433, ('沙鹿區 433')),
    (434, ('龍井區 434')),
    (435, ('梧棲區 435')),
    (436, ('清水區 436')),
    (437, ('大甲區 437')),
    (438, ('外埔區 438')),
    (439, ('大安區 439')),
    (500, ('彰化市 500')),
    (502, ('芬園鄉 502')),
    (503, ('花壇鄉 503')),
    (504, ('秀水鄉 504')),
    (505, ('鹿港鎮 505')),
    (506, ('福興鄉 506')),
    (507, ('線西鄉 507')),
    (508, ('和美鎮 508')),
    (509, ('伸港鄉 509')),
    (510, ('員林鎮 510')),
    (511, ('社頭鄉 511')),
    (512, ('永靖鄉 512')),
    (513, ('埔心鄉 513')),
    (514, ('溪湖鎮 514')),
    (515, ('大村鄉 515')),
    (516, ('埔鹽鄉 516')),
    (520, ('田中鎮 520')),
    (521, ('北斗鎮 521')),
    (522, ('田尾鄉 522')),
    (523, ('埤頭鄉 523')),
    (524, ('溪州鄉 524')),
    (525, ('竹塘鄉 525')),
    (526, ('二林鎮 526')),
    (527, ('大城鄉 527')),
    (528, ('芳苑鄉 528')),
    (530, ('二水鄉 530')),
    (540, ('南投市 540')),
    (541, ('中寮鄉 541')),
    (542, ('草屯鎮 542')),
    (544, ('國姓鄉 544')),
    (545, ('埔里鎮 545')),
    (546, ('仁愛鄉 546')),
    (551, ('名間鄉 551')),
    (552, ('集集鎮 552')),
    (553, ('水里鄉 553')),
    (555, ('魚池鄉 555')),
    (556, ('信義鄉 556')),
    (557, ('竹山鎮 557')),
    (558, ('鹿谷鄉 558')),
    (600, ('東　區 600')),
    (600, ('西　區 600')),
    (602, ('番路鄉 602')),
    (603, ('梅山鄉 603')),
    (604, ('竹崎鄉 604')),
    (605, ('阿里山 605')),
    (606, ('中埔鄉 606')),
    (607, ('大埔鄉 607')),
    (608, ('水上鄉 608')),
    (611, ('鹿草鄉 611')),
    (612, ('太保市 612')),
    (613, ('朴子市 613')),
    (614, ('東石鄉 614')),
    (615, ('六腳鄉 615')),
    (616, ('新港鄉 616')),
    (621, ('民雄鄉 621')),
    (622, ('大林鎮 622')),
    (623, ('溪口鄉 623')),
    (624, ('義竹鄉 624')),
    (625, ('布袋鎮 625')),
    (630, ('斗南鎮 630')),
    (631, ('大埤鄉 631')),
    (632, ('虎尾鎮 632')),
    (633, ('土庫鎮 633')),
    (634, ('褒忠鄉 634')),
    (635, ('東勢鄉 635')),
    (636, ('台西鄉 636')),
    (637, ('崙背鄉 637')),
    (638, ('麥寮鄉 638')),
    (640, ('斗六市 640')),
    (643, ('林內鄉 643')),
    (646, ('古坑鄉 646')),
    (647, ('莿桐鄉 647')),
    (648, ('西螺鎮 648')),
    (649, ('二崙鄉 649')),
    (651, ('北港鎮 651')),
    (652, ('水林鄉 652')),
    (653, ('口湖鄉 653')),
    (654, ('四湖鄉 654')),
    (655, ('元長鄉 655')),
    (700, ('中西區 700')),
    (701, ('東　區 701')),
    (702, ('南　區 702')),
    (704, ('北　區 704')),
    (708, ('安平區 708')),
    (709, ('安南區 709')),
    (710, ('永康區 710')),
    (711, ('歸仁區 711')),
    (712, ('新化區 712')),
    (713, ('左鎮區 713')),
    (714, ('玉井區 714')),
    (715, ('楠西區 715')),
    (716, ('南化區 716')),
    (717, ('仁德區 717')),
    (718, ('關廟區 718')),
    (719, ('龍崎區 719')),
    (720, ('官田區 720')),
    (721, ('麻豆區 721')),
    (722, ('佳里區 722')),
    (723, ('西港區 723')),
    (724, ('七股區 724')),
    (725, ('將軍區 725')),
    (726, ('學甲區 726')),
    (727, ('北門區 727')),
    (730, ('新營區 730')),
    (731, ('後壁區 731')),
    (732, ('白河區 732')),
    (733, ('東山區 733')),
    (734, ('六甲區 734')),
    (735, ('下營區 735')),
    (736, ('柳營區 736')),
    (737, ('鹽水區 737')),
    (741, ('善化區 741')),
    (742, ('大內區 742')),
    (743, ('山上區 743')),
    (744, ('新市區 744')),
    (745, ('安定區 745')),
    (800, ('新興區 800')),
    (801, ('前金區 801')),
    (802, ('苓雅區 802')),
    (803, ('鹽埕區 803')),
    (804, ('鼓山區 804')),
    (805, ('旗津區 805')),
    (806, ('前鎮區 806')),
    (807, ('三民區 807')),
    (811, ('楠梓區 811')),
    (812, ('小港區 812')),
    (813, ('左營區 813')),
    (814, ('仁武區 814')),
    (815, ('大社區 815')),
    (820, ('岡山區 820')),
    (821, ('路竹區 821')),
    (822, ('阿蓮區 822')),
    (823, ('田寮區 823')),
    (824, ('燕巢區 824')),
    (825, ('橋頭區 825')),
    (826, ('梓官區 826')),
    (827, ('彌陀區 827')),
    (828, ('永安區 828')),
    (829, ('湖內區 829')),
    (830, ('鳳山區 830')),
    (831, ('大寮區 831')),
    (832, ('林園區 832')),
    (833, ('鳥松區 833')),
    (840, ('大樹區 840')),
    (842, ('旗山區 842')),
    (843, ('美濃區 843')),
    (844, ('六龜區 844')),
    (845, ('內門區 845')),
    (846, ('杉林區 846')),
    (847, ('甲仙區 847')),
    (848, ('桃源區 848')),
    (849, ('那瑪夏 849')),
    (851, ('茂林區 851')),
    (852, ('茄萣區 852')),
    (880, ('馬公市 880')),
    (881, ('西嶼鄉 881')),
    (882, ('望安鄉 882')),
    (883, ('七美鄉 883')),
    (884, ('白沙鄉 884')),
    (885, ('湖西鄉 885')),
    (890, ('金沙鎮 890')),
    (891, ('金湖鎮 891')),
    (892, ('金寧鄉 892')),
    (893, ('金城鎮 893')),
    (894, ('烈嶼鄉 894')),
    (896, ('烏坵鄉 896')),
    (900, ('屏東市 900')),
    (901, ('三地門 901')),
    (902, ('霧台鄉 902')),
    (903, ('瑪家鄉 903')),
    (904, ('九如鄉 904')),
    (905, ('里港鄉 905')),
    (906, ('高樹鄉 906')),
    (907, ('鹽埔鄉 907')),
    (908, ('長治鄉 908')),
    (909, ('麟洛鄉 909')),
    (911, ('竹田鄉 911')),
    (912, ('內埔鄉 912')),
    (913, ('萬丹鄉 913')),
    (920, ('潮州鎮 920')),
    (921, ('泰武鄉 921')),
    (922, ('來義鄉 922')),
    (923, ('萬巒鄉 923')),
    (924, ('崁頂鄉 924')),
    (925, ('新埤鄉 925')),
    (926, ('南州鄉 926')),
    (927, ('林邊鄉 927')),
    (928, ('東港鎮 928')),
    (929, ('琉球鄉 929')),
    (931, ('佳冬鄉 931')),
    (932, ('新園鄉 932')),
    (940, ('枋寮鄉 940')),
    (941, ('枋山鄉 941')),
    (942, ('春日鄉 942')),
    (943, ('獅子鄉 943')),
    (944, ('車城鄉 944')),
    (945, ('牡丹鄉 945')),
    (946, ('恆春鎮 946')),
    (947, ('滿州鄉 947')),
    (950, ('台東市 950')),
    (951, ('綠島鄉 951')),
    (952, ('蘭嶼鄉 952')),
    (953, ('延平鄉 953')),
    (954, ('卑南鄉 954')),
    (955, ('鹿野鄉 955')),
    (956, ('關山鎮 956')),
    (957, ('海端鄉 957')),
    (958, ('池上鄉 958')),
    (959, ('東河鄉 959')),
    (961, ('成功鎮 961')),
    (962, ('長濱鄉 962')),
    (963, ('太麻里 963')),
    (964, ('金峰鄉 964')),
    (965, ('大武鄉 965')),
    (966, ('達仁鄉 966')),
    (970, ('花蓮市 970')),
    (971, ('新城鄉 971')),
    (972, ('秀林鄉 972')),
    (973, ('吉安鄉 973')),
    (974, ('壽豐鄉 974')),
    (975, ('鳳林鎮 975')),
    (976, ('光復鄉 976')),
    (977, ('豐濱鄉 977')),
    (978, ('瑞穗鄉 978')),
    (979, ('萬榮鄉 979')),
    (981, ('玉里鎮 981')),
    (982, ('卓溪鄉 982')),
    (983, ('富里鄉 983')),
)
