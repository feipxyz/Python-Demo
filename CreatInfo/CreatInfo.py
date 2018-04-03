# -*- coding: utf-8 -*-

from lxml import etree
from enum import Enum, unique

INVALIDNUM = -999

@unique
class MapValueType(Enum):
    Barrier = -1
    Road = 0
    Bin = 1
    Shelf = 2
    Shelf_half = 3
    Shelf_full = 4
    Work = 10
    Battery = 11
    Buffer = 12
    Spin = 13
    Spin2 = 14
    Block = 15
    High_way = 16
    Turnning = 17
    Park = 19
    Buffer_bin = 20
    Buffer_cross = 21
    Lift_cross = 22
    Head_cross = 23
    End_cross = 24
    Recover_cross = 25
    Map_cross = 26
    Corridor = 27
    Self_cross = 28
    Buffer_elevatoe = 31


class PointInfo(object):
    __slots__ = ('direction', 'mask', 'xpos_offset', 'ypos_offset', 'x', 'y')


class GridMap(object):
    def __init__(self):
        self.path = ''
        self.free_pos = []

    def set_xml_path(self, path):
        self._path = path

    def set_xml_content(self):
        pass

    def parse_map_content(self):
        parser = etree.XMLParser(load_dtd=True)
        tree = etree.parse(self._path, parser)
        root = tree.getroot()

        position = []

        for elemnt in root:
            if elemnt.tag == 'ErrorCode':
                self.errorcode = elemnt.text
            elif elemnt.tag == 'MapName':
                self.map_name = elemnt.text
            elif elemnt.tag == 'Row':
                self.map_row = elemnt.text
            elif elemnt.tag == 'Col':
                self.map_col = elemnt.text
            elif elemnt.tag == 'LeftBottomPos':
                for left_bottom_pos in elemnt:
                    if left_bottom_pos.tag == 'Row':
                        self.left_bottom_pos_x = left_bottom_pos.text
                    elif left_bottom_pos.tag == 'Col':
                        self.left_bottom_pos_y = left_bottom_pos.text
            elif elemnt.tag == 'RowInfo':
                row_pos = []
                for mask in elemnt:
                    if mask.tag == 'Mask':
                        pos = PointInfo()
                        pos.mask = int(mask.text)
                        pos.direction = int(mask.get('Direction'))
                        pos.xpos_offset = mask.get('fXposOffset', default=INVALIDNUM)
                        pos.ypos_offset = mask.get('fXposOffset', default=INVALIDNUM)
                        pos.x = None
                        pos.y = None
                        row_pos.append(pos)
                position.append(row_pos)

        for i, row in enumerate(position):
            for j, pos in enumerate(row):
                pos.x = j
                pos.y = i

                if (pos.mask == MapValueType.Bin.value or pos.mask == MapValueType.Shelf.value or
                    pos.mask == MapValueType.Shelf_half.value or pos.mask == MapValueType.Shelf_full.value):
                    self.free_pos.append(pos)



def get_robot_num():
    has_get = False
    input_str = input("请输入小车数量：")

    if input_str == 'x':
        exit()

    try:
        robot_num = int(input_str)
        has_get = True
    except:
        print("输入不合法, 请重新输入")
        has_get = False

    return has_get, input_str


def get_map_info(path):
    pass


if __name__ == '__main__':

    grid_map = GridMap()
    grid_map.set_xml_path('mr_map.xml')
    grid_map.parse_map_content()

    pass

    # while 1:
    #     has_get, robot_num = get_robot_num()
    #     if has_get == True:
    #         break
