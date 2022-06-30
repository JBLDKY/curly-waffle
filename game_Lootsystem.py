
import pygame
from pygame.locals import *
from game_Constants import *
import sys
import pygame.image
import pygame.key
import random
import math
from mousefunctionality import *
pygame.init()
pygame.font.init()
# from plsondtdie import screen

###Tier governs stat AMOUNT
###Rarity governs amount of unique STATS
st1_spr_group = helm_t1_spr_group = chest_t1_spr_group = shield_t1_spr_group = ring_t1_spr_group = pygame.sprite.Group()
st1_spr_list = helm_t1_spr_list = chest_t1_spr_list = shield_t1_spr_list = ring_t1_spr_list = []

# helm_t1_spr_group = pygame.sprite.Group()
# helm_t1_spr_list = []
# chest_t1_spr_group = pygame.sprite.Group()
# chest_t1_spr_list = []
# ring_t1_spr_group = pygame.sprite.Group()
# ring_t1_spr_list = []
# shield_t1_spr_group = pygame.sprite.Group()
# shield_t1_spr_list = []
# myArray = ["sword1", "sword2", "sword3", "sword4"]
st2_spr_group = pygame.sprite.Group()
inventory_list = []
inventory_sprite_group = pygame.sprite.Group()
inventory_spr_list = []
inventory_spr_group = pygame.sprite.Group()

# idlist = []
# swordlist = []
# numswordlist = ['sword0', 'sword1', 'sword2', 'sword3', 'sword4', 'sword5', 'sword6', 'sword7', 'sword8', 'sword9', 'sword10', 'sword11', 'sword12', 'sword13', 'sword14', 'sword15', 'sword16', 'sword17', 'sword18', 'sword19', 'sword20', 'sword21', 'sword22', 'sword23', 'sword24', 'sword25', 'sword26', 'sword27', 'sword28', 'sword29', 'sword30', 'sword31', 'sword32', 'sword33', 'sword34', 'sword35', 'sword36', 'sword37', 'sword38', 'sword39', 'sword40', 'sword41', 'sword42', 'sword43', 'sword44', 'sword45', 'sword46', 'sword47', 'sword48', 'sword49', 'sword50', 'sword51', 'sword52', 'sword53', 'sword54', 'sword55', 'sword56', 'sword57', 'sword58', 'sword59', 'sword60', 'sword61', 'sword62', 'sword63', 'sword64', 'sword65', 'sword66', 'sword67', 'sword68', 'sword69', 'sword70', 'sword71', 'sword72', 'sword73', 'sword74', 'sword75', 'sword76', 'sword77', 'sword78', 'sword79', 'sword80', 'sword81', 'sword82', 'sword83', 'sword84', 'sword85', 'sword86', 'sword87', 'sword88', 'sword89', 'sword90', 'sword91', 'sword92', 'sword93', 'sword94', 'sword95', 'sword96', 'sword97', 'sword98', 'sword99', 'sword100', 'sword101', 'sword102', 'sword103', 'sword104', 'sword105', 'sword106', 'sword107', 'sword108', 'sword109', 'sword110', 'sword111', 'sword112', 'sword113', 'sword114', 'sword115', 'sword116', 'sword117', 'sword118', 'sword119', 'sword120', 'sword121', 'sword122', 'sword123', 'sword124', 'sword125', 'sword126', 'sword127', 'sword128', 'sword129', 'sword130', 'sword131', 'sword132', 'sword133', 'sword134', 'sword135', 'sword136', 'sword137', 'sword138', 'sword139', 'sword140', 'sword141', 'sword142', 'sword143', 'sword144', 'sword145', 'sword146', 'sword147', 'sword148', 'sword149', 'sword150', 'sword151', 'sword152', 'sword153', 'sword154', 'sword155', 'sword156', 'sword157', 'sword158', 'sword159', 'sword160', 'sword161', 'sword162', 'sword163', 'sword164', 'sword165', 'sword166', 'sword167', 'sword168', 'sword169', 'sword170', 'sword171', 'sword172', 'sword173', 'sword174', 'sword175', 'sword176', 'sword177', 'sword178', 'sword179', 'sword180', 'sword181', 'sword182', 'sword183', 'sword184', 'sword185', 'sword186', 'sword187', 'sword188', 'sword189', 'sword190', 'sword191', 'sword192', 'sword193', 'sword194', 'sword195', 'sword196', 'sword197', 'sword198', 'sword199', 'sword200', 'sword201', 'sword202', 'sword203', 'sword204', 'sword205', 'sword206', 'sword207', 'sword208', 'sword209', 'sword210', 'sword211', 'sword212', 'sword213', 'sword214', 'sword215', 'sword216', 'sword217', 'sword218', 'sword219', 'sword220', 'sword221', 'sword222', 'sword223', 'sword224', 'sword225', 'sword226', 'sword227', 'sword228', 'sword229', 'sword230', 'sword231', 'sword232', 'sword233', 'sword234', 'sword235', 'sword236', 'sword237', 'sword238', 'sword239', 'sword240', 'sword241', 'sword242', 'sword243', 'sword244', 'sword245', 'sword246', 'sword247', 'sword248', 'sword249', 'sword250', 'sword251', 'sword252', 'sword253', 'sword254', 
# 'sword255', 'sword256', 'sword257', 'sword258', 'sword259', 'sword260', 'sword261', 'sword262', 'sword263', 'sword264', 'sword265', 'sword266', 'sword267', 'sword268', 'sword269', 'sword270', 'sword271', 'sword272', 'sword273', 'sword274', 'sword275', 'sword276', 'sword277', 'sword278', 'sword279', 'sword280', 'sword281', 'sword282', 'sword283', 'sword284', 'sword285', 'sword286', 'sword287', 'sword288', 'sword289', 'sword290', 'sword291', 'sword292', 'sword293', 'sword294', 'sword295', 'sword296', 'sword297', 'sword298', 'sword299', 'sword300', 'sword301', 'sword302', 'sword303', 'sword304', 'sword305', 'sword306', 'sword307', 'sword308', 'sword309', 'sword310', 'sword311', 'sword312', 'sword313', 'sword314', 'sword315', 'sword316', 'sword317', 'sword318', 'sword319', 'sword320', 'sword321', 'sword322', 'sword323', 'sword324', 'sword325', 'sword326', 'sword327', 'sword328', 'sword329', 'sword330', 'sword331', 'sword332', 'sword333', 'sword334', 'sword335', 'sword336', 'sword337', 'sword338', 'sword339', 'sword340', 'sword341', 'sword342', 'sword343', 'sword344', 'sword345', 'sword346', 'sword347', 'sword348', 'sword349', 'sword350', 'sword351', 'sword352', 'sword353', 'sword354', 'sword355', 'sword356', 'sword357', 'sword358', 'sword359', 'sword360', 'sword361', 'sword362', 'sword363', 'sword364', 'sword365', 'sword366', 'sword367', 'sword368', 'sword369', 'sword370', 'sword371', 'sword372', 'sword373', 'sword374', 'sword375', 'sword376', 'sword377', 'sword378', 'sword379', 'sword380', 'sword381', 'sword382', 'sword383', 'sword384', 'sword385', 'sword386', 'sword387', 'sword388', 'sword389', 'sword390', 'sword391', 'sword392', 'sword393', 'sword394', 'sword395', 'sword396', 'sword397', 'sword398', 'sword399', 'sword400', 'sword401', 'sword402', 'sword403', 'sword404', 'sword405', 'sword406', 'sword407', 'sword408', 'sword409', 'sword410', 'sword411', 'sword412', 'sword413', 'sword414', 'sword415', 'sword416', 'sword417', 'sword418', 'sword419', 'sword420', 'sword421', 'sword422', 'sword423', 'sword424', 'sword425', 'sword426', 'sword427', 'sword428', 'sword429', 'sword430', 'sword431', 'sword432', 'sword433', 'sword434', 'sword435', 'sword436', 'sword437', 'sword438', 'sword439', 'sword440', 'sword441', 'sword442', 'sword443', 'sword444', 'sword445', 'sword446', 'sword447', 'sword448', 'sword449', 'sword450', 'sword451', 'sword452', 'sword453', 'sword454', 'sword455', 'sword456', 'sword457', 'sword458', 'sword459', 'sword460', 'sword461', 'sword462', 'sword463', 'sword464', 'sword465', 'sword466', 'sword467', 'sword468', 'sword469', 'sword470', 'sword471', 'sword472', 'sword473', 'sword474', 'sword475', 'sword476', 'sword477', 'sword478', 'sword479', 'sword480', 'sword481', 
# 'sword482', 'sword483', 'sword484', 'sword485', 'sword486', 'sword487', 'sword488', 'sword489', 'sword490', 'sword491', 'sword492', 'sword493', 'sword494', 'sword495', 'sword496', 'sword497', 'sword498', 'sword499', 'sword500', 'sword501', 'sword502', 'sword503', 'sword504', 'sword505', 'sword506', 'sword507', 'sword508', 'sword509', 'sword510', 'sword511', 'sword512', 'sword513', 'sword514', 'sword515', 'sword516', 'sword517', 'sword518', 'sword519', 'sword520', 'sword521', 'sword522', 'sword523', 'sword524', 'sword525', 'sword526', 'sword527', 'sword528', 'sword529', 'sword530', 'sword531', 'sword532', 'sword533', 'sword534', 'sword535', 'sword536', 'sword537', 'sword538', 'sword539', 'sword540', 'sword541', 'sword542', 'sword543', 'sword544', 'sword545', 'sword546', 'sword547', 'sword548', 'sword549', 'sword550', 'sword551', 'sword552', 'sword553', 'sword554', 'sword555', 'sword556', 'sword557', 'sword558', 'sword559', 'sword560', 'sword561', 'sword562', 'sword563', 'sword564', 'sword565', 'sword566', 'sword567', 'sword568', 'sword569', 'sword570', 'sword571', 'sword572', 'sword573', 'sword574', 'sword575', 'sword576', 'sword577', 'sword578', 'sword579', 'sword580', 'sword581', 'sword582', 'sword583', 'sword584', 'sword585', 'sword586', 'sword587', 'sword588', 'sword589', 'sword590', 'sword591', 'sword592', 'sword593', 'sword594', 'sword595', 'sword596', 'sword597', 'sword598', 'sword599', 'sword600', 'sword601', 'sword602', 'sword603', 'sword604', 'sword605', 'sword606', 'sword607', 'sword608', 'sword609', 'sword610', 'sword611', 'sword612', 'sword613', 'sword614', 'sword615', 'sword616', 'sword617', 'sword618', 'sword619', 'sword620', 'sword621', 'sword622', 'sword623', 'sword624', 'sword625', 'sword626', 'sword627', 'sword628', 'sword629', 'sword630', 'sword631', 'sword632', 'sword633', 'sword634', 'sword635', 'sword636', 'sword637', 'sword638', 'sword639', 'sword640', 'sword641', 'sword642', 'sword643', 'sword644', 'sword645', 'sword646', 'sword647', 'sword648', 'sword649', 'sword650', 'sword651', 'sword652', 'sword653', 'sword654', 'sword655', 'sword656', 'sword657', 'sword658', 'sword659', 'sword660', 'sword661', 'sword662', 'sword663', 'sword664', 'sword665', 'sword666', 'sword667', 'sword668', 'sword669', 'sword670', 'sword671', 'sword672', 'sword673', 'sword674', 'sword675', 'sword676', 'sword677', 'sword678', 'sword679', 'sword680', 'sword681', 'sword682', 'sword683', 'sword684', 'sword685', 'sword686', 'sword687', 'sword688', 'sword689', 'sword690', 'sword691', 'sword692', 'sword693', 'sword694', 'sword695', 'sword696', 'sword697', 'sword698', 'sword699', 'sword700', 'sword701', 'sword702', 'sword703', 'sword704', 'sword705', 'sword706', 'sword707', 'sword708', 
# 'sword709', 'sword710', 'sword711', 'sword712', 'sword713', 'sword714', 'sword715', 'sword716', 'sword717', 'sword718', 'sword719', 'sword720', 'sword721', 'sword722', 'sword723', 'sword724', 'sword725', 'sword726', 'sword727', 'sword728', 'sword729', 'sword730', 'sword731', 'sword732', 'sword733', 'sword734', 'sword735', 'sword736', 'sword737', 'sword738', 'sword739', 'sword740', 'sword741', 'sword742', 'sword743', 'sword744', 'sword745', 'sword746', 'sword747', 'sword748', 'sword749', 'sword750', 'sword751', 'sword752', 'sword753', 'sword754', 'sword755', 'sword756', 'sword757', 'sword758', 'sword759', 'sword760', 'sword761', 'sword762', 'sword763', 'sword764', 'sword765', 'sword766', 'sword767', 'sword768', 'sword769', 'sword770', 'sword771', 'sword772', 'sword773', 'sword774', 'sword775', 'sword776', 'sword777', 'sword778', 'sword779', 'sword780', 'sword781', 'sword782', 'sword783', 'sword784', 'sword785', 'sword786', 'sword787', 'sword788', 'sword789', 'sword790', 'sword791', 'sword792', 'sword793', 'sword794', 'sword795', 'sword796', 'sword797', 'sword798', 'sword799', 'sword800', 'sword801', 'sword802', 'sword803', 'sword804', 'sword805', 'sword806', 'sword807', 'sword808', 'sword809', 'sword810', 'sword811', 'sword812', 'sword813', 'sword814', 'sword815', 'sword816', 'sword817', 'sword818', 'sword819', 'sword820', 'sword821', 'sword822', 'sword823', 'sword824', 'sword825', 'sword826', 'sword827', 'sword828', 'sword829', 'sword830', 'sword831', 'sword832', 'sword833', 'sword834', 'sword835', 'sword836', 'sword837', 'sword838', 'sword839', 'sword840', 'sword841', 'sword842', 'sword843', 'sword844', 'sword845', 'sword846', 'sword847', 'sword848', 'sword849', 'sword850', 'sword851', 'sword852', 'sword853', 'sword854', 'sword855', 'sword856', 'sword857', 'sword858', 'sword859', 'sword860', 'sword861', 'sword862', 'sword863', 'sword864', 'sword865', 'sword866', 'sword867', 'sword868', 'sword869', 'sword870', 'sword871', 'sword872', 'sword873', 'sword874', 'sword875', 'sword876', 'sword877', 'sword878', 'sword879', 'sword880', 'sword881', 'sword882', 'sword883', 'sword884', 'sword885', 'sword886', 'sword887', 'sword888', 'sword889', 'sword890', 'sword891', 'sword892', 'sword893', 'sword894', 'sword895', 'sword896', 'sword897', 'sword898', 'sword899', 'sword900', 'sword901', 'sword902', 'sword903', 'sword904', 'sword905', 'sword906', 'sword907', 'sword908', 'sword909', 'sword910', 'sword911', 'sword912', 'sword913', 'sword914', 'sword915', 'sword916', 'sword917', 'sword918', 'sword919', 'sword920', 'sword921', 'sword922', 'sword923', 'sword924', 'sword925', 'sword926', 'sword927', 'sword928', 'sword929', 'sword930', 'sword931', 'sword932', 'sword933', 'sword934', 'sword935', 
# 'sword936', 'sword937', 'sword938', 'sword939', 'sword940', 'sword941', 'sword942', 'sword943', 'sword944', 'sword945', 'sword946', 'sword947', 'sword948', 'sword949', 'sword950', 'sword951', 'sword952', 'sword953', 'sword954', 'sword955', 'sword956', 'sword957', 'sword958', 'sword959', 'sword960', 'sword961', 'sword962', 'sword963', 'sword964', 'sword965', 'sword966', 'sword967', 'sword968', 'sword969', 'sword970', 'sword971', 'sword972', 'sword973', 'sword974', 'sword975', 'sword976', 'sword977', 'sword978', 'sword979', 'sword980', 'sword981', 'sword982', 'sword983', 'sword984', 'sword985', 'sword986', 'sword987', 'sword988', 'sword989', 'sword990', 'sword991', 'sword992', 'sword993', 'sword994', 'sword995', 'sword996', 'sword997', 'sword998', 'sword999']
color_list = ["grey", "green", "blue", "purple"]
# def numbergen():
#     for x in range (1000):
#         idlist.append(x)

#     for x in range (1000):
#         swordlist.append("sword")

#     for x in range (1000):
#         numswordlist.append(swordlist[x] + str(idlist[x]))
#     # print(numswordlist)
        
# numbergen()
##attempt to do it  in a class system
# s1, s2, s3, s4, s5, s6, s7, s8, s9, s10 = None, None, None, None, None, None, None, None, None, None 
# scall_array = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
####SWORDS#####
class sword(pygame.sprite.Sprite):
    def __init__(self, attack, a_speed, lifesteal, health_regen, health, stun, name, image, x_pos, y_pos, equiptype, rarity):
        super(sword, self).__init__()
        self.attack = attack 
        self.a_speed = a_speed
        self.lifesteal = lifesteal
        self.health_regen = health_regen
        self.max_health = health
        self.stun = stun
        self.stat_list = [self.attack, self.a_speed, self.lifesteal, self.health_regen, self.max_health, self.stun]
        self.stat_list_names = ["attack", "atk. speed", "lifesteal", "health regen", "health", "stun"]
        self.tooltip_list = []
        self.name = name 
        self.image = image
        self.rect = image.get_rect()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect.center = [x_pos, y_pos]
        self.equiptype = equiptype
        self.rarity = rarity
        self.name_color = color_list[self.rarity]
    def setloc(self, x, y):
        self.rect.center = [x, y]
    def draw_rarity_border(self):
        pygame.draw.rect(screen, self.name_color, self.rect, 5)
    def make_tooltip(self):
        self.tooltip_list = []
        for x in range(len(self.stat_list)):
            if self.stat_list[x] > 0:
                self.tooltip_list.append([self.stat_list_names[x], self.stat_list[x]])
    def tooltip(self):
        return self.tooltip_list, self.name_color

class chest(pygame.sprite.Sprite):
    def __init__(self, block, evade, lifesteal, health_regen, health, stun, counter, spikes, taunt, defense, name, image, x_pos, y_pos, equiptype, rarity):
        super(chest, self).__init__()
        self.evade = evade
        self.block = block
        self.lifesteal = lifesteal
        self.health_regen = health_regen
        self.max_health = health
        self.defense = defense
        self.stun = stun 
        self.counter = counter
        self.spikes = spikes
        self.taunt = taunt
        self.stat_list = [self.evade, self.block, self.lifesteal, self.health_regen, self.max_health, self.defense, self.stun, self.counter, self.taunt, self.spikes]
        self.stat_list_names = ["evade", "block", "lifesteal", "health regen", "health", "defense", "stun", "counter", "taunt", "spikes"]
        self.tooltip_list = []
        self.name = name 
        self.image = image
        self.rect = image.get_rect()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect.center = [x_pos, y_pos]
        self.equiptype = "chest" 
        self.rarity = rarity
        self.name_color = color_list[self.rarity]
    def setloc(self, x, y):
        self.rect.center = [x, y]
    def draw_rarity_border(self):
        pygame.draw.rect(screen, self.name_color, self.rect, 5)
    def make_tooltip(self):
        self.tooltip_list = []
        for x in range(len(self.stat_list)):
            if self.stat_list[x] > 0:
                self.tooltip_list.append([self.stat_list_names[x], self.stat_list[x]])
    def tooltip(self):
        return self.tooltip_list, self.name_color

class ring(pygame.sprite.Sprite):
    def __init__(self, attack, cleave, lifesteal, health_regen, health, defense, crit, crit_damage, name, image, x_pos, y_pos, equiptype, rarity):
        super(ring, self).__init__()
        self.attack = attack
        self.cleave = cleave
        self.lifesteal = lifesteal
        self.health_regen = health_regen
        self.max_health = health
        self.defense = defense
        self.crit = crit
        self.crit_damage = crit_damage
        self.stat_list = [self.attack, self.cleave, self.lifesteal, self.health_regen, self.max_health, self.defense, self.crit, self.crit_damage]
        self.stat_list_names = ["attack", "cleave", "lifesteal", "health regen", "health", "defense", "crit", "crit_damage"]
        self.tooltip_list = []
        self.name = name 
        self.image = image
        self.rect = image.get_rect()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect.center = [x_pos, y_pos]
        self.equiptype = equiptype
        self.rarity = rarity
        self.name_color = color_list[self.rarity]
    def setloc(self, x, y):
        self.rect.center = [x, y]
    def draw_rarity_border(self):
        pygame.draw.rect(screen, self.name_color, self.rect, 5)
    def make_tooltip(self):
        self.tooltip_list = []
        for x in range(len(self.stat_list)):
            if self.stat_list[x] > 0:
                self.tooltip_list.append([self.stat_list_names[x], self.stat_list[x]])
    def tooltip(self):
        return self.tooltip_list, self.name_color

class shield(pygame.sprite.Sprite):
    def __init__(self, block, evade, lifesteal, health_regen, health, defense, stun, counter, spikes, taunt, name, image, x_pos, y_pos, equiptype, rarity):
        super(shield, self).__init__()
        self.block = block
        self.evade = evade
        self.lifesteal = lifesteal
        self.health_regen = health_regen
        self.max_health = health
        self.defense = defense
        self.stun = stun
        self.counter = counter
        self.spikes = spikes 
        self.taunt = taunt
        self.stat_list = [self.block, self.evade, self.lifesteal, self.health_regen, self.max_health, self.defense, self.stun, self.counter, self.spikes, self.taunt]
        self.stat_list_names = ["block", "evade", "lifesteal", "health regen", "health", "defense", "stun", "counter", "spikes", "taunt"]
        self.tooltip_list = []
        self.name = name 
        self.image = image
        self.rect = image.get_rect()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect.center = [x_pos, y_pos]
        self.equiptype = "shield" 
        self.rarity = rarity
        self.name_color = color_list[self.rarity]
    def setloc(self, x, y):
        self.rect.center = [x, y]
    def draw_rarity_border(self):
        pygame.draw.rect(screen, self.name_color, self.rect, 5)
    def make_tooltip(self):
        self.tooltip_list = []
        for x in range(len(self.stat_list)):
            if self.stat_list[x] > 0:
                self.tooltip_list.append([self.stat_list_names[x], self.stat_list[x]])
    def tooltip(self):
        return self.tooltip_list, self.name_color

class helm(pygame.sprite.Sprite):
    def __init__(self, evade, block, lifesteal, health_regen, health, defense, name, image, x_pos, y_pos, equiptype, rarity):
        super(helm, self).__init__()
        self.evade = evade
        self.block = block
        self.lifesteal = lifesteal
        self.health_regen = health_regen
        self.max_health = health
        self.defense = defense
        self.stat_list = [self.evade, self.block, self.lifesteal, self.health_regen, self.max_health, self.defense]
        self.stat_list_names = ["evade", "block", "lifesteal", "health regen", "health", "defense"]
        self.tooltip_list = []
        self.name = name 
        self.image = image
        self.rect = image.get_rect()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect.center = [x_pos, y_pos]
        self.equiptype = "helm"
        self.rarity = rarity
        self.name_color = color_list[self.rarity]
    def setloc(self, x, y):
        self.rect.center = [x, y]
    def draw_rarity_border(self):
        pygame.draw.rect(screen, self.name_color, self.rect, 5)
    def make_tooltip(self):
        self.tooltip_list = []
        for x in range(len(self.stat_list)):
            if self.stat_list[x] > 0:
                self.tooltip_list.append([self.stat_list_names[x], self.stat_list[x]])
    def tooltip(self):
        return self.tooltip_list, self.name_color
####CHEST################################
# class chest_w(pygame.sprite.Sprite):
#     def __init__(self, defense, health, evade, health_regen, block, lifesteal, , name, image, x_pos, y_pos, equiptype):
#         super(sword, self).__init__()
#         self.attack = attack 
#         self.a_speed = a_speed
#         self.lifesteal = lifesteal
#         self.health_regen = health_regen
#         self.health = health
#         self.stun = stun
#         self.name = name 
#         self.image = image
#         self.rect = image.get_rect()
#         self.x_pos = x_pos
#         self.y_pos = y_pos
#         self.rect.center = [x_pos, y_pos]
#         self.equiptype = equiptype
#     def setloc(self, x, y):
#         self.rect.center = [x, y]
#     def tooltip(self):
#         displaynumbercenter("name","", self.name, "red", 15, 900,300) 
#         displaynumbercenter("attack","attack: ", self.attack, "red", 15, 900,300) 
#         displaynumbercenter("a_speed","atk. spd: ", self.a_speed, "red", 15, 900,315) 
#         displaynumbercenter("lifesteal","lifesteal: ", self.lifesteal, "red", 15, 900,330) 
#         displaynumbercenter("health_regen","health regen: ", self.health_regen, "red", 15, 900,345) 
#         displaynumbercenter("health","health: ", self.health, "red", 15, 900,360) 
#         displaynumbercenter("stun","stun: ", self.stun, "red", 15, 900,375) 

def displaynumbercenter(name, prefix, text, color, size, x, y):
    apply_size = pygame.font.Font("C:\WINDOWS\Fonts\cambriab.ttf", size) #picks the font and the size, only the size is variable
    str_text = prefix + str(text)   #stringifies the integer
    rendered_text = apply_size.render(str_text, False, color) #converts text to image
    name = rendered_text.get_rect(center = (x, y)) #assign the text a rectangle in variable "name          
    return (rendered_text, name)



#Name, Image, xpos, ypos, equiptype should always be rolled. The other stats are selected at random, equal chance, 1 per rarity tier. Therefore, rarity should be rolled before
# anything else so that then can be decided how many random stats should be rolled for optimal speed. 

def roll_helms_t1(amount):
    rarity_dist = [70, 19, 11, 2]
    rarity_list = [0, 1, 2, 3] 
    stats_list = ["block", "evade", "lifesteal", "health_regen", "health", "defense"]
    for x in range(amount):
        rarity = random.choices(rarity_list, weights = rarity_dist, k = 1)
        stats_chosen = random.sample(stats_list, (rarity[0]+1))
        r_block = r_evade = r_lifesteal = r_health_regen = r_health = r_defense = 0

        if "block" in stats_chosen:
            r_block = random.randint(1, 4)

        if "evade" in stats_chosen:
            r_evade = random.randint(4, 9)

        if "lifesteal" in stats_chosen:
            r_lifesteal = random.randint(1, 2)

        if "health_regen" in stats_chosen:
            r_health_regen = random.randint(1, 2)

        if "health" in stats_chosen:
            r_health = random.randint(15, 50)

        if "defense" in stats_chosen:
            r_defense = random.randint(3, 7)

        r_name = name_helm_array[math.floor(random.random()*len(name_helm_array))]
        r_img = img_helm_array[math.floor(random.random()*len(img_helm_array))]
        r_x_pos = 500
        r_y_pos = 500
        r_equiptype = "helm"
        r_rarity = rarity[0]
        
        helmt1 = helm(r_evade, r_block, r_lifesteal, r_health_regen, r_health, r_defense, r_name, r_img, r_x_pos, r_y_pos, r_equiptype, r_rarity)
        helmt1.make_tooltip()
    ### list
        helm_t1_spr_list.append(helmt1)
        helm_t1_spr_group.add(helmt1)
        drop_loot(helmt1)

def roll_rings_t1(amount):
    rarity_dist = [1, 18, 80, 1]
    rarity_list = [0, 1, 2, 3] 
    stats_list = ["attack", "cleave", "lifesteal", "health_regen", "health", "defense", "crit", "crit damage"]
    for x in range(amount):
        ####MAYBE LOWER TIER ITEMS SHOULD HAVE LESS "FUN" STATS#####
        rarity = random.choices(rarity_list, weights = rarity_dist, k = 1)
        stats_chosen = random.sample(stats_list, (rarity[0]+1))
        r_attack = r_cleave = r_lifesteal = r_health_regen = r_health = r_defense = r_crit = r_crit_damage = 0

        if "attack" in stats_chosen:
            r_attack = random.randint(1, 4)

        if "cleave" in stats_chosen:
            r_cleave = random.randint(4, 9)

        if "lifesteal" in stats_chosen:
            r_lifesteal = random.randint(1, 2)

        if "health_regen" in stats_chosen:
            r_health_regen = random.randint(1, 2)

        if "health" in stats_chosen:
            r_health = random.randint(15, 50)

        if "defense" in stats_chosen:
            r_defense = random.randint(3, 7)

        if "crit" in stats_chosen:
            r_crit = random.randint(3, 7)

        if "crit damage" in stats_chosen:
            r_crit_damage = random.randint(3, 7)

        r_name = name_ring_array[math.floor(random.random()*len(name_ring_array))]
        r_img = img_ring_array[math.floor(random.random()*len(img_ring_array))]
        r_x_pos = 500
        r_y_pos = 500
        r_equiptype = "ring"
        r_rarity = rarity[0]
        
        ringt1 = ring(r_attack, r_cleave, r_lifesteal, r_health_regen, r_health, r_defense, r_crit, r_crit_damage, r_name, r_img, r_x_pos, r_y_pos, r_equiptype, r_rarity)
        ringt1.make_tooltip()
    ### list
        ring_t1_spr_list.append(ringt1)
        ring_t1_spr_group.add(ringt1)

        drop_loot(ringt1)

def roll_chest_t1(amount):
    rarity_dist = [70, 19, 10, 1]
    rarity_list = [0, 1, 2, 3] 
    stats_list = ["block", "evade", "lifesteal", "health_regen", "health", "stun", "counter", "spikes", "taunt"]
    for x in range(amount):
        rarity = random.choices(rarity_list, weights = rarity_dist, k = 1)
        stats_chosen = random.sample(stats_list, (rarity[0]+1))
        r_block = r_evade = r_lifesteal = r_health_regen = r_health = r_stun = r_counter = r_spikes = r_taunt = r_defense = 0

        if "block" in stats_chosen:
            r_block = random.randint(1, 4)

        if "evade" in stats_chosen:
            r_evade = random.randint(4, 9)

        if "lifesteal" in stats_chosen:
            r_lifesteal = random.randint(1, 2)

        if "health_regen" in stats_chosen:
            r_health_regen = random.randint(1, 2)

        if "health" in stats_chosen:
            r_health = random.randint(15, 50)

        if "stun" in stats_chosen:
            r_stun = random.randint(3, 7)

        if "counter" in stats_chosen:
            r_counter = random.randint(3, 7)

        if "spikes" in stats_chosen:
            r_spikes = random.randint(3, 7)

        if "taunt" in stats_chosen:
            r_taunt = random.randint(3, 7)

        if "defense" in stats_chosen:
            r_defense = random.randint(3, 7)

        r_name = name_chest_array[math.floor(random.random()*len(name_chest_array))]
        r_img = img_chest_array[math.floor(random.random()*len(img_chest_array))]
        r_x_pos = 500
        r_y_pos = 500
        r_equiptype = "chest"
        r_rarity = rarity[0]
        
        chestt1 = chest(r_block, r_evade, r_lifesteal, r_health_regen, r_health, r_stun, r_counter, r_spikes, r_taunt, r_defense, r_name, r_img, r_x_pos, r_y_pos, r_equiptype, r_rarity)
        chestt1.make_tooltip()
    ### list
        chest_t1_spr_list.append(chestt1)
        chest_t1_spr_group.add(chestt1)

        drop_loot(chestt1)

def roll_shield_t1(amount):
    rarity_dist = [70, 19, 10, 1]
    rarity_list = [0, 1, 2, 3] 
    stats_list = ["block", "evade", "lifesteal", "health_regen", "health", "stun", "counter", "spikes", "taunt"]
    for x in range(amount):
        rarity = random.choices(rarity_list, weights = rarity_dist, k = 1)
        stats_chosen = random.sample(stats_list, (rarity[0]+1))
        r_block = r_evade = r_lifesteal = r_health_regen = r_health = r_defense = r_stun = r_counter = r_spikes = r_taunt = 0

        if "block" in stats_chosen:
            r_block = random.randint(1, 4)

        if "evade" in stats_chosen:
            r_evade = random.randint(4, 9)

        if "lifesteal" in stats_chosen:
            r_lifesteal = random.randint(1, 2)

        if "health_regen" in stats_chosen:
            r_health_regen = random.randint(1, 2)

        if "health" in stats_chosen:
            r_health = random.randint(15, 50)

        if "defense" in stats_chosen:
            r_defense = random.randint(15, 50)

        if "stun" in stats_chosen:
            r_stun = random.randint(3, 7)

        if "counter" in stats_chosen:
            r_counter = random.randint(3, 7)

        if "spikes" in stats_chosen:
            r_spikes = random.randint(3, 7)

        if "taunt" in stats_chosen:
            r_taunt = random.randint(3, 7)

        r_name = name_shield_array[math.floor(random.random()*len(name_shield_array))]
        r_img = img_shield_array[math.floor(random.random()*len(img_shield_array))]
        r_x_pos = 500
        r_y_pos = 500
        r_equiptype = "shield"
        r_rarity = rarity[0]
        
        shieldt1 = shield(r_block, r_evade, r_lifesteal, r_health_regen, r_health, r_defense, r_stun, r_counter, r_spikes, r_taunt, r_name, r_img, r_x_pos, r_y_pos, r_equiptype, r_rarity)
        shieldt1.make_tooltip()
    ### list
        shield_t1_spr_list.append(shieldt1)
        shield_t1_spr_group.add(shieldt1)
        drop_loot(shieldt1)

def roll_swords_t1(amount):
    rarity_dist = [70, 19, 10, 1]
    rarity_list = [0, 1, 2, 3] 
    stats_list = ["attack", "a_speed", "lifesteal", "health_regen", "health", "stun"]
    for x in range(amount):
        rarity = random.choices(rarity_list, weights = rarity_dist, k = 1)
        stats_chosen = random.sample(stats_list, (rarity[0]+1))
        r_attack = r_a_speed = r_lifesteal = r_health_regen = r_health = r_stun = 0

        if "attack" in stats_chosen:
            r_attack = random.randint(1, 4)

        if "a_speed" in stats_chosen:
            r_a_speed = random.randint(4, 9)

        if "lifesteal" in stats_chosen:
            r_lifesteal = random.randint(1, 2)

        if "health_regen" in stats_chosen:
            r_health_regen = random.randint(1, 2)

        if "health" in stats_chosen:
            r_health = random.randint(15, 50)

        if "stun" in stats_chosen:
            r_stun = random.randint(3, 7)

        r_name = name_sword_array[math.floor(random.random()*len(name_sword_array))]
        r_img = img_sword_array[math.floor(random.random()*len(img_sword_array))]
        r_x_pos = 500
        r_y_pos = 500
        r_equiptype = "weapon"
        r_rarity = rarity[0]
        
        swordt1 = sword(r_attack, r_a_speed, r_lifesteal, r_health_regen, r_health, r_stun, r_name, r_img, r_x_pos, r_y_pos, r_equiptype, r_rarity)
        swordt1.make_tooltip()
    ### list
        st1_spr_list.append(swordt1)
        st1_spr_group.add(swordt1)

        drop_loot(swordt1)
### group 
# 
### group 
        
# # def roll_swords_t2(amount):
#     global st2_spr_group; st2_spr_list
#     for x in range(amount):
#         r_attack = 4
#         r_a_speed = 5
#         r_lifesteal = 2
#         r_health_regen = 3
#         r_health = 111
#         r_stun = 4
#         r_name = "BronzeSword"
#         r_img = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\sword1.png").convert()
#         r_x_pos = 500
#         r_y_pos = 500
        
#         penis2 = sword(r_attack, r_a_speed, r_lifesteal, r_health_regen, r_health, r_stun, r_name, r_img, r_x_pos, r_y_pos)
#         st2_spr_group.add(penis2)
#         st2_spr_list.insert(penis2) 
        
# print(st1_spr_list[0])
# roll_swords_t2(4)

def sortloot():
    if len(inventory_list) < 1:
        return
    inventory_list[0].setloc(1400, 300)
    if len(inventory_list) < 2:
        return
    inventory_list[1].setloc(1454, 300)
    if len(inventory_list) < 3:
        return
    inventory_list[2].setloc(1508, 300)
    if len(inventory_list) < 4:
        return
    inventory_list[3].setloc(1562, 300)
    if len(inventory_list) < 5:
        return
    inventory_list[4].setloc(1400, 354)
    if len(inventory_list) < 6:
        return
    inventory_list[5].setloc(1454, 354)
    if len(inventory_list) < 7:
        return
    inventory_list[6].setloc(1508, 354)
    if len(inventory_list) < 8:
        return
    inventory_list[7].setloc(1562, 354)
    if len(inventory_list) < 9:
        return
    inventory_list[8].setloc(1400, 408)
    if len(inventory_list) < 10:
        return
    inventory_list[9].setloc(1454, 408)
    if len(inventory_list) < 11:
        return
    inventory_list[10].setloc(1508, 408)
    if len(inventory_list) < 12:
        return  
    inventory_list[11].setloc(1562, 408)

    
def drop_loot(item):
    # global inventory_spr_group
    global st1_spr_list, st1_spr_group, inventory_spr_group
    ###INVENTORY LIST
    # inventory_spr_group.empty()
    invspace = int(12 - len(inventory_list)) 
    # roll_swords_t1(amount) #generate loot
    # deleteexistinglootamount = len(st1_spr_list) - invspace
    if invspace == 0:
        inventory_spr_group.remove(inventory_list[0])
        del inventory_list[0]
        
    inventory_list.append(item) #append inventory list with the generated loot list
    inventory_spr_group.add(item)
    
    # for i in range(0, deleteexistinglootamount):
    #     inventory_spr_group.remove(inventory_list[i])
        
    # # if invspace - len(st1_spr_list) < 0:
    #     del inventory_list[0: int(deleteexistinglootamount)]
        
    # st1_spr_list = []
    ###SORTLOOT
    sortloot()
# int_drop = 0
# tier1_drop_dict = { 
#     "helmt1" : roll_swords_t1(int_drop),
#     "ringst1" : roll_rings_t1(x),
#     "swordst1" : roll_swords_t1(x),
#     "chestt1" : roll_chest_t1(x),
#     "shieldt1" : roll_shield_t1(x)
    
    # }

def loot_table(loopcount, enemy_tier):
    ####enemy_tier = [drop_chance, drop_quant, rarity modifier]
#### There should be a chance to hit the loot table upon killing an enemy. There should be a separate chance calculation for deteremining the amount of drops. 
#### The amount of drops should be pretty big, because the chance to hit the loot table in the first place is rather small. 
#### Rarity should maybe also be affected by some data the enemy has. 
    loopcount = loopcount 
    enemy_tier = enemy_tier
#### fix ^ later ^ ####

    drop_chance = 100
    # drop_quant = random.randint(1, 3)
    drop_quant = 1
    # drop_table = ["helmt1", "ringst1", "swordst1", "chestt1", "shieldt1"]   
    # random.shuffle(drop_table)

    if drop_chance/100 >= random.random():
        for x in range(drop_quant):
            roll_item = random.random()
            if 0 <= roll_item < 0.2:
                roll_swords_t1(1)
            if 0.2 <= roll_item < 0.4:
                roll_rings_t1(1)
            if 0.4 <= roll_item < 0.6:
                roll_chest_t1(1)
            if 0.6 <= roll_item < 0.8:
                roll_shield_t1(1)
            if 0.8 <= roll_item < 1:
                roll_helms_t1(1)

            # drop_table[math.floor(random.random() * len(drop_table))]

        
        
        
    # if drop_chance/100 >= random.random():
    #     for x in range(drop_quant):
    #         roll_helms_t1()
    #         roll_rings_t1()
    #         roll_chest_t1()
    #         roll_shield_t1()

# def sortloot():
#     for x in range(inventory_list):
#         inventory_list[x].setloc(inventory)

# inventory_spr_group.add(inventory_list)
# print(inventory_spr_group)


##scales with monster and loop level
##TIER1
t1_cards = [None, ]
t1_gear = [None, ]
t1_resources = [None, ]
t1_collectibles = [None,]
t1_uniques = [None,]


##TIER2

##TIER3

#TIER4























#DELETED:

# def roll_swords_t1_backup(amount):
#     global st1_spr_group; st1_spr_list
#     amount = amount
#     # numbergen()
#     for x in range(amount):
#         r_attack = random.randint(1, 4)
#         r_a_speed = random.randint(4, 9)
#         r_lifesteal = random.randint(1, 2)
#         r_health_regen = random.randint(1, 2)
#         r_health = random.randint(15, 50)
#         r_stun = random.randint(3, 7)
#         r_name = name_sword_array[math.floor(random.random()*len(name_sword_array))]
#         r_img = img_sword_array[math.floor(random.random()*len(img_sword_array))]
#         r_x_pos = 500
#         r_y_pos = 500
#         r_equiptype = "weapon"
        
#         swordt1 = sword(r_attack, r_a_speed, r_lifesteal, r_health_regen, r_health, r_stun, r_name, r_img, r_x_pos, r_y_pos, r_equiptype)
# ### list
#         st1_spr_list.append(swordt1)
#         st1_spr_group.add(swordt1)
#         return st1_spr_list, st1_spr_group, amount