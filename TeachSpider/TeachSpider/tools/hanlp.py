# -*- coding: utf-8 -*-
# @Time    : 2019/4/28 21:39
# @Author  : 郭增祥
# @File    : hanlp-百度学术信息挖掘
from pyhanlp import *
import re


class hanlp(object):
    def __init__(self):
        pass

    def set_a_list(self, a):
        # 目前只想到这儿直接返回，可能需要在这儿进行处理
        return self.parse(a)

    def parse(self, aa):
        temp = []
        for a in aa:
            name = hanlp.IsName(a[0])
            if name is not False:  # 如果判断是姓名，则返回非 False
                a[0] = name  # 如果里面有姓名则更新a[0]里面字段
                temp.append(a)
        return temp

    @classmethod
    def IsName(cls, a_name):
        # 判断当前是否是姓名，并滤除里面有姓名的，注意，此法及其依赖hanlp的命名实体识别
        # 注意，只找到第一个可能是姓名的字段，直接返回
        for ss in HanLP.segment(a_name):
            if ss.nature.name =="nr":
                return ss.word
        return False
if __name__ == '__main__':
    s =[['中文版', 'http://mgx.imu.edu.cn/index.htm'], ['English', 'http://mgx.imu.edu.cn/yw/HOME.htm'], ['蒙文版', 'http://mgx.imu.edu.cn/mw/mengwen1.htm'], ['首页', 'http://mgx.imu.edu.cn/index.htm'], ['学院概况', 'http://mgx.imu.edu.cn/xygk/xyjj.htm'], ['学院简介', 'http://mgx.imu.edu.cn/xygk/xyjj.htm'], ['历任领导', 'http://mgx.imu.edu.cn/xygk/lrld.htm'], ['现任领导', 'http://mgx.imu.edu.cn/xygk/xrld.htm'], ['教授委员会', 'http://mgx.imu.edu.cn/xygk/jswyh.htm'], ['总支委员会', 'http://mgx.imu.edu.cn/xygk/zzwyh.htm'], ['联系我们', 'http://mgx.imu.edu.cn/xygk/lxwm.htm'], ['机构设置', 'http://mgx.imu.edu.cn/jgsz/mgyywxx.htm'], ['蒙古语言文学系', 'http://mgx.imu.edu.cn/jgsz/mgyywxx.htm'], ['新闻出版学系', 'http://mgx.imu.edu.cn/jgsz/xwcbxx.htm'], ['蒙古历史学系', 'http://mgx.imu.edu.cn/jgsz/mglsxx.htm'], ['蒙古语文研究所', 'http://mgx.imu.edu.cn/jgsz/mgywyjs.htm'], ['蒙古史研究所', 'http://mgx.imu.edu.cn/jgsz/mgsyjs.htm'], ['内蒙古近现代史研究所', 'http://mgx.imu.edu.cn/jgsz/nmgjxdsyjs.htm'], ['蒙古文化研究所', 'http://mgx.imu.edu.cn/jgsz/mgwhyjs.htm'], ['公共教学部', 'http://mgx.imu.edu.cn/jgsz/ggjxb.htm'], ['行政办公室', 'http://mgx.imu.edu.cn/jgsz/xzbgs.htm'], ['教务办公室', 'http://mgx.imu.edu.cn/jgsz/jwbgs.htm'], ['团总支（学工办）', 'http://mgx.imu.edu.cn/jgsz/tzz_xgb_.htm'], ['资料室', 'http://mgx.imu.edu.cn/jgsz/zls.htm'], ['师资队伍', 'http://mgx.imu.edu.cn/szdw/mgyywxx.htm'], ['蒙古语言文学系', 'http://mgx.imu.edu.cn/szdw/mgyywxx.htm'], ['新闻出版学系', 'http://mgx.imu.edu.cn/szdw/xwcbxx.htm'], ['蒙古历史学系', 'http://mgx.imu.edu.cn/szdw/mglsxx.htm'], ['公共课教学部', 'http://mgx.imu.edu.cn/szdw/ggkjxb.htm'], ['蒙古语文研究所', 'http://mgx.imu.edu.cn/szdw/mgywyjs.htm'], ['蒙古文化研究所', 'http://mgx.imu.edu.cn/szdw/mgwhyjs.htm'], ['管理岗', 'http://mgx.imu.edu.cn/szdw/glg.htm'], ['教辅岗', 'http://mgx.imu.edu.cn/szdw/jfg.htm'], ['人才培养', 'http://mgx.imu.edu.cn/rcpy/bkspy1/mgyywx.htm'], ['本科生培养', 'http://mgx.imu.edu.cn/rcpy/bkspy1/mgyywx.htm'], ['硕士生培养', 'http://mgx.imu.edu.cn/rcpy/ssspy1/zgssmzyywx.htm'], ['博士生培养', 'http://mgx.imu.edu.cn/rcpy/bsspy1/zgyywx.htm'], ['留学生培养', 'http://mgx.imu.edu.cn/rcpy/lxspy.htm'], ['博士后流动站', 'http://mgx.imu.edu.cn/rcpy/bshldz.htm'], ['科学研究', 'http://mgx.imu.edu.cn/kxyj/kyxm.htm'], ['科研项目', 'http://mgx.imu.edu.cn/kxyj/kyxm.htm'], ['获奖成果', 'http://mgx.imu.edu.cn/kxyj/hjcg.htm'], ['科研平台', 'http://mgx.imu.edu.cn/kxyj/kypt1/yyyyxyjzx.htm'], ['社会服务', 'http://mgx.imu.edu.cn/shfw.htm'], ['党建工作', 'http://mgx.imu.edu.cn/djgz/dzzgk.htm'], ['党总支概况', 'http://mgx.imu.edu.cn/djgz/dzzgk.htm'], ['团总支概况', 'http://mgx.imu.edu.cn/djgz/tzzgk.htm'], ['工会概况', 'http://mgx.imu.edu.cn/djgz/ghgk.htm'], ['学生会概况', 'http://mgx.imu.edu.cn/djgz/xshgk.htm'], ['学生社团概况', 'http://mgx.imu.edu.cn/djgz/xsstgk1/wygwxs.htm'], ['两学一做', 'http://mgx.imu.edu.cn/djgz/lxyz.htm'], ['政治理论学习', 'http://mgx.imu.edu.cn/djgz/zzllxx.htm'], ['蒙古语言文学系', 'http://mgx.imu.edu.cn/szdw/mgyywxx.htm'], ['新闻出版学系', 'http://mgx.imu.edu.cn/szdw/xwcbxx.htm'], ['蒙古历史学系', 'http://mgx.imu.edu.cn/szdw/mglsxx.htm'], ['公共课教学部', 'http://mgx.imu.edu.cn/szdw/ggkjxb.htm'], ['蒙古语文研究所', 'http://mgx.imu.edu.cn/szdw/mgywyjs.htm'], ['蒙古文化研究所', 'http://mgx.imu.edu.cn/szdw/mgwhyjs.htm'], ['管理岗', 'http://mgx.imu.edu.cn/szdw/glg.htm'], ['教辅岗', 'http://mgx.imu.edu.cn/szdw/jfg.htm'], ['首页', 'http://mgx.imu.edu.cn/index.htm'], ['师资队伍', 'http://mgx.imu.edu.cn/szdw/mgyywxx.htm'], ['额尔敦白音', 'http://mgx.imu.edu.cn/info/1312/2076.htm'], ['布仁巴图', 'http://mgx.imu.edu.cn/info/1312/1687.htm'], ['呼日勒巴特尔', 'http://mgx.imu.edu.cn/info/1312/1686.htm'], ['额尔很巴雅尔', 'http://mgx.imu.edu.cn/info/1312/1685.htm'], ['乌日斯嘎拉', 'http://mgx.imu.edu.cn/info/1312/1684.htm'], ['丁玉龙', 'http://mgx.imu.edu.cn/info/1312/1776.htm'], ['塔亚', 'http://mgx.imu.edu.cn/info/1312/1683.htm'], ['图门吉日嘎拉', 'http://mgx.imu.edu.cn/info/1312/1682.htm'], ['仁图雅', 'http://mgx.imu.edu.cn/info/1312/1681.htm'], ['玉荣', 'http://mgx.imu.edu.cn/info/1312/1680.htm'], ['正月', 'http://mgx.imu.edu.cn/info/1312/1679.htm'], ['斯琴托雅', 'http://mgx.imu.edu.cn/info/1313/1689.htm'], ['额尔敦朝鲁', 'http://mgx.imu.edu.cn/info/1313/1688.htm'], ['哈斯巴特尔', 'http://mgx.imu.edu.cn/info/1314/1693.htm'], ['阚海英', 'http://mgx.imu.edu.cn/info/1314/1692.htm'], ['敖道呼', 'http://mgx.imu.edu.cn/info/1314/1691.htm'], ['玉杰', 'http://mgx.imu.edu.cn/info/1314/1690.htm'], ['', 'http://bszs.conac.cn/sitename?method=show&id=319B028B5F7A01E5E053012819ACF26B'], ['蒙ICP16002391号-1', 'http://www.miitbeian.gov.cn/publish/query/indexFirst.action']]
    han = hanlp()
    print(han.set_a_list(s))
