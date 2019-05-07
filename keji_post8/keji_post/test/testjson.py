# -*- coding: utf-8 -*-
# @Time    : 2019/4/4 14:07
# @Author  : 郭增祥
# @File    : testjson-教师信息挖掘
# @Pakage  :
import json
import jmespath
import ast
my = str({
	"code":"200",
	"data":{
		"adminPosition":"教授",
		"code":"A0117",
		"conclusionAbstract":"",
		"dependUintID":"100391",
		"dependUnit":"南京大学",
		"downloadHref":"",
		"projectAbstractC":"",
		"projectAbstractE":"",
		"projectAdmin":"何旭初",
		"projectAdminID":"644437",
		"projectKeywordC":"线性规划;非线性规划;计算方法.",
		"projectKeywordE":"",
		"projectName":"大型线性和非线性规划的计算方法",
		"projectType":"218",
		"ratifyNo":"18971045",
		"researchTimeScope":"1990-01-01 00:00:00.0到1992-12-31 00:00:00.0",
		"resultsList":[],
		"supportNum":"2"
	},
	"message":"Success"
})
data = {'name':'zz', 'books':[{'name':'x','price':1}, {'name':'y', 'price':2,'tag':'t'}]}
nomal = {
	"code":200,
	"data":{
		"adminPosition":"副教授",
		"code":"F012005",
		"conclusionAbstract":"为满足当前电子系统多功能、小型化、集成化的紧迫需求，小型化微波滤波器的研发工作正在不断推进。然而，小型化会引起损耗增加、Q值降低、功率密度升高等问题，这使得滤波器的边带变圆滑、通带不平坦、频率选择性降低、功率容量降级。为此，本项目系统研究了用低Q谐振器以有限额外插损为代价实现高性能有耗滤波器的综合设计方法、诊断调试技术和功率容量特性。本项目取得的主要成果包括：1）提出了结合预失真、阻性和复耦合系数、非一致Q值、灵敏度分析等技术的有耗滤波器综合方法，采用双模/多模微带、基片集成波导等混合结构实现，获得了具有平坦通带特性的高性能有耗带通滤波器；2）通过人为调控滤波器中的损耗分布，解析设计出具有负群时延特性的吸收式带阻滤波器、具有稳定插入损耗的电可调负群时延电路，并利用阻性交叉耦合改善了多端口滤波网络的端口隔离特性，基于频变耦合设计了高频率选择性四路滤波功分器；3）针对有耗滤波器Q值低、耦合系数多为复数、拓扑结构复杂的特点，提出了从其仿真和测试结果提取有耗耦合矩阵和电路模型并确定其参数定量关系的诊断和调试技术，满足因果性、无源性、可实现性等，编制了多款通用软件；4）研究了有耗滤波器的电热耦合机理，提出了电阻和谐振器上热耗散的紧凑模型，预测其带外功率容量，给出全波电热仿真结果进行验证，进而分析各种典型有耗滤波器所适合的不同功率等级应用场景；5）基于多层PCB和LTCC工艺，实现了多款三维混合结构的小型化有耗滤波器。基于本项目成果已发表和录用论文25篇，申请专利6项，登记软件著作权5项，培养研究生7名。综上所述，本项目已形成了一整套高性能小型化有耗滤波器设计、实现、诊断、验证、功率容量评估的方法。",
		"dependUintID":"100027",
		"dependUnit":"上海交通大学",
		"downloadHref":"",
		"projectAbstractC":"多功能集成是当前电子信息技术的重要趋势，这要求通讯系统关键部件微波滤波器不断向高性能和小型化方向飞速发展。有耗滤波器可用较低Q值谐振器以牺牲有限的插损为代价实现高Q滤波器的带内平坦、边带陡峭和零点尖锐特性，是小型化无源元件的首选方案之一。本项目拟在青年基金小型化无源元件电热分析与功率容量研究基础上，系统探究有耗滤波器的设计与三维实现方法及其功率容量问题。具体包括：1）研究结合预失真、有耗综合、非一致Q值等技术的有耗滤波器综合和优化方法；2）研究基于混合结构、高Q介质加载、嵌入元件的高性能小型化有耗滤波器三维集成方案；3）研究从仿测结果提取有耗滤波器耦合矩阵和电路模型并确定其参数化定量关系的有效诊断和调试技术；4）研究有耗滤波器中电热耦合和无源交调的多物理机理，预测其功率容量。本项目拟提供高性能小型化有耗滤波器设计、实现、诊断和验证的整套技术，将功率容量要求结合到设计中实现性能的协同优化。",
		"projectAbstractE":"Multifunctional integration has been one of the important trends of modern electronic information technology, which requires the microwave filter, one of the key components in communication systems, keep the rapid developments of high performance and miniaturization. A lossy filter can be designed with low-Q resonators to achieve flat in-band response, steep band transition and sharp zeros as a high-Q filter, only at the expense of its limited insertion loss. Therefore, it has become one of the most attractive solutions for miniaturized passives. Based on the investigations on electro-thermal fields and power handling capabilities of miniaturized passive components in the applicant’s Youth Science Foundation, this project is mainly focused on the systematical investigations on the design methods, 3D realizations and power handling capabilities of lossy filters, especially including: 1) the synthesis and optimization methods of lossy filters combined with several promising techniques, such as predistortion, lossy synthesis and non-uniform Q-factor; 2) the 3D integration schemes of high-performance miniaturized lossy filters, based on hybrid structure, high-Q dielectric loading and embedded passives, etc.; 3) the effective methods for diagnosing and tuning lossy filters, to extract their coupling matrices and circuit models from the simulated and measured results and to further obtain the quantitative relationships between the critical parameters and performances; 4) the multi-physical mechanisms of electro-thermal coupling and passive intermodulation in lossy filters, and the prediction of their power handling capabilities. By this project, we intend to build up a complete technology for the design, implementation, diagnosis and verification of high-performance miniaturized lossy filters, where the requirement on power handling capability will also be incorporated with the design procedure, so as to achieve the collaborative optimization for all the concerns.",
		"projectAdmin":"吴林晟",
		"projectAdminID":"764947",
		"projectKeywordC":"有耗滤波器设计;功率容量;耦合矩阵;三维集成;滤波器诊断调试",
		"projectKeywordE":"lossy filter design;power handling capability;coupling matrix;3-D integration;filter diagnosis and tuning",
		"projectName":"高性能小型化有耗滤波器设计及其功率容量研究",
		"projectType":"218",
		"ratifyNo":"61370008",
		"researchTimeScope":"2014-01-01 00:00:00.0到2017-12-31 00:00:00.0",
		"resultsList":[
			{
				"result":[
					"1",
					"ZD3017284",
					"Diagnosis and tuning of filtering antenna based on extracted coupling matrix",
					"会议论文",
					"Zhou, Hua-Hua(#)，<b>Wu, Lin-Sheng</b>(*)，Mao, Jun-Fa，Tang, Min"
				]
			},
			{
				"result":[
					"2",
					"ZD3016396",
					"Substrate integrated waveguide filter with flat passband based on complex couplings",
					"期刊论文",
					"Liang-Feng Qiu(#)，<b>Lin-Sheng Wu</b>(*)，Wen-Yan Yin，Jun-Fa Mao"
				]
			},
			{
				"result":[
					"3",
					"1000008984860",
					"A lossy triple-mode microstrip filter with flat passband based on nonuniform Q-factors",
					"会议论文",
					"Feng-Jun Chen(#)，<b>Lin-Sheng Wu</b>(*)，Liang-Feng Qiu，Jun-Fa Mao"
				]
			},
			{
				"result":[
					"4",
					"1000018398412",
					"A Flat-Passband Microstrip Filter With Nonuniform-Q Dual-Mode Resonators",
					"期刊论文",
					"Qiu, Liang-Feng(#)，<b>Wu, Lin-Sheng</b>(*)，Yin, Wen-Yan(*)，Mao, Jun-Fa"
				]
			},
			{
				"result":[
					"5",
					"ZD3022377",
					"A fully planar broadband rat-race coupler with stepped-impedance and coupled microstrip lines",
					"会议论文",
					"Bo-Yuan Wang(#)，<b>Lin-Sheng Wu</b>(*)，Tao Guan，Liang-Feng Qiu，Jun-Fa Mao"
				]
			},
			{
				"result":[
					"6",
					"ZD3019448",
					"Wideband filters on high-resistivity silicon substrate for 5G high-frequency applications",
					"会议论文",
					"<b>Lin-Sheng Wu</b>(#)(*)，Jun-Fa Mao，Fang Hou，Jian Zhu"
				]
			},
			{
				"result":[
					"7",
					"1000021907204",
					"Absorptive Bandstop Filter With Prescribed Negative Group Delay and Bandwidth",
					"期刊论文",
					"Qiu, Liang-Feng(#)(*)，<b>Wu, Lin-Sheng</b>，Yin, Wen-Yan，Mao, Jun-Fa"
				]
			},
			{
				"result":[
					"8",
					"1000014782753",
					"Flat-passband substrate integrated waveguide filterwith resistive couplings",
					"期刊论文",
					"Bin Gao(#)，<b>Lin-Sheng Wu</b>(*)，Jun-Fa Mao"
				]
			},
			{
				"result":[
					"9",
					"ZD3023233",
					"A Negative Group Delay Tuner with Stable Insertion Loss",
					"会议论文",
					"<b>Lin-Sheng Wu</b>(#)(*)，Liang-Feng Qiu，Jun-Fa Mao"
				]
			},
			{
				"result":[
					"10",
					"ZD3018374",
					"Lossy substrate integrated waveguide (SIW) filter with improved passband flatness",
					"会议论文",
					"Bin Gao(#)，<b>Lin-Sheng Wu</b>(*)，Jun-Fa Mao"
				]
			},
			{
				"result":[
					"11",
					"ZD3035880",
					"滤波器诊断软件",
					"软件著作权",
					"<b>吴林晟</b>，邱良丰，毛军发"
				]
			},
			{
				"result":[
					"12",
					"ZD3016204",
					"Hybrid non-uniform-Q lossy filters with substrate integrated waveguide and microstrip resonators",
					"期刊论文",
					"Liang-Feng Qiu(#)，<b>Lin-Sheng Wu</b>(*)，Wen-Yan Yin，Jun-Fa Mao"
				]
			},
			{
				"result":[
					"13",
					"ZD3207167",
					"基于耦合矩阵的滤波天线研究",
					"人才培养",
					""
				]
			},
			{
				"result":[
					"14",
					"ZD3207233",
					"小型化微波滤波器的诊断与调试方法研究",
					"人才培养",
					""
				]
			},
			{
				"result":[
					"15",
					"ZD3202609",
					"小型化带内平坦有耗滤波器的分析与设计方法研究",
					"人才培养",
					""
				]
			},
			{
				"result":[
					"16",
					"ZD3035650",
					"无载品质因素计算器软件",
					"软件著作权",
					"<b>吴林晟</b>，邱良丰，毛军发"
				]
			},
			{
				"result":[
					"17",
					"ZD3021715",
					"A balanced-to-balanced filtering Gysel power divider with unequal power division",
					"会议论文",
					"Bo-Yuan Wang(#)，Xiang-Yu Wang，<b>Lin-Sheng Wu</b>(*)，Jun-Fa Mao"
				]
			},
			{
				"result":[
					"18",
					"ZD3114428",
					"一种抑制高速电路地弹噪声的超宽带平面电磁带隙结构",
					"专利",
					"李晓春(#)(*)，张佶，毛军发"
				]
			},
			{
				"result":[
					"19",
					"1000008984673",
					"A planar microstrip crossover with lumped inductors for three intersecting channels",
					"期刊论文",
					"<b>Wu, Lin-Sheng</b>(#)(*)，Guo, Yong-Xin，Mao, Jun-Fa"
				]
			},
			{
				"result":[
					"20",
					"19909740705",
					"Noununiform Scaling Technique for Parallel-Coupled Pairs Lossy Filters",
					"会议论文",
					"Qiu, Liang-Feng(#)，<b>Wu, Lin-Sheng</b>(*)，Yin, Wen-Yan，Mao, Jun-Fa"
				]
			},
			{
				"result":[
					"21",
					"ZD3018846",
					"A filter with equal-ripple negative group delay",
					"会议论文",
					"Liang-Feng Qiu(#)，<b>Lin-Sheng Wu</b>(*)，Wen-Yan Yin，Jun-Fa Mao"
				]
			},
			{
				"result":[
					"22",
					"ZD3035324",
					"基于交叉耦合抑制通道间互耦的滤波天线的实现方法",
					"专利",
					"<b>吴林晟</b>(#)(*)，毛军发"
				]
			},
			{
				"result":[
					"23",
					"1000008984874",
					"Lossy filter with uniform Q-factors by optimization method",
					"会议论文",
					"Liang-Feng Qiu(#)，<b>Lin-Sheng Wu</b>(*)，Wen-Yan Yin，Jun-Fa Mao"
				]
			},
			{
				"result":[
					"24",
					"ZD3035586",
					"有耗滤波器综合软件",
					"软件著作权",
					"<b>吴林晟</b>，邱良丰，毛军发"
				]
			},
			{
				"result":[
					"25",
					"ZD3112719",
					"共形双频段收发天线",
					"专利",
					"沈广海(#)，李静，彭宏利(*)，<b>吴林晟</b>"
				]
			},
			{
				"result":[
					"26",
					"ZD3022746",
					"A novel multifunctional quadrature hybrid coupler",
					"会议论文",
					"Bo-Yuan Wang(#)，<b>Lin-Sheng Wu</b>(*)，Jun-Fa Mao"
				]
			},
			{
				"result":[
					"27",
					"ZD3024564",
					"A wideband quadrature hybrid coupler with unequal power division and harmonic suppression",
					"会议论文",
					"Verona Chanu Maibam(#)，Bo-Yuan Wang，<b>Lin-Sheng Wu</b>(*)，Jun-Fa Mao"
				]
			},
			{
				"result":[
					"28",
					"ZD3198901",
					"平面有耗滤波器综合与设计方法研究",
					"人才培养",
					""
				]
			},
			{
				"result":[
					"29",
					"ZD3023791",
					"公度线滤波器的自动化设计调试方法",
					"会议论文",
					"汤宇伟(#)，<b>吴林晟</b>(*)，邱良丰，毛军发"
				]
			},
			{
				"result":[
					"30",
					"ZD3202729",
					"新型混合耦合器研究",
					"人才培养",
					""
				]
			},
			{
				"result":[
					"31",
					"19906969446",
					"Cutoff Frequency of Substrate Integrated Waveguide with Single-Walled Carbon Nanotube Bundle Vias",
					"会议论文",
					"<b>Wu, Lin-Sheng</b>(#)(*)，Tang, Min，Mao, Jun-Fa"
				]
			},
			{
				"result":[
					"32",
					"1000013904071",
					"High-selectivitytriband bandpass filter based on dual-plane microstrip/slotline structure",
					"期刊论文",
					"Li-Yun Shi(#)(*)，Ning Wang，<b>Lin-Sheng Wu</b>"
				]
			},
			{
				"result":[
					"33",
					"ZD3035273",
					"基于公度传输线网络的双通带滤波器",
					"专利",
					"<b>吴林晟</b>(#)(*)，张仕强，汤宇伟，毛军发"
				]
			},
			{
				"result":[
					"34",
					"ZD3024211",
					"一种用于433MHz 射频发射前端的天线及相关电路设计",
					"会议论文",
					"王一童(#)，张凌峰，汤宇伟，史丽云(*)，<b>吴林晟</b>"
				]
			},
			{
				"result":[
					"35",
					"ZD3202453",
					"小型化有耗和频变耦合滤波器研究",
					"人才培养",
					""
				]
			},
			{
				"result":[
					"36",
					"ZD3114082",
					"基片集成同轴波导互连阵列结构",
					"专利",
					"李晓春(#)(*)，邵妍，王宁，袁斌，毛军发"
				]
			},
			{
				"result":[
					"37",
					"ZD3035396",
					"具有稳定插入损耗的电可调负群时延电路",
					"专利",
					"<b>吴林晟</b>(#)(*)，邱良丰，毛军发"
				]
			},
			{
				"result":[
					"38",
					"ZD3035754",
					"S参数去嵌软件",
					"软件著作权",
					"<b>吴林晟</b>，邱良丰，毛军发"
				]
			},
			{
				"result":[
					"39",
					"1000013904126",
					"A four-way microstrip filtering power divider with frequency-dependent couplings",
					"期刊论文",
					"Feng-Jun Chen(#)，<b>Lin-Sheng Wu</b>(*)，Liang-Feng Qiu，Jun-Fa Mao"
				]
			},
			{
				"result":[
					"40",
					"1000008984734",
					"A hybrid method for flat-passband filter with nonuniform Q resonators and predistortion",
					"会议论文",
					"Liang-Feng Qiu，<b>Lin-Sheng Wu</b>(*)，Wen-Yan Yin"
				]
			},
			{
				"result":[
					"41",
					"ZD3035505",
					"带阻滤波器综合软件",
					"软件著作权",
					"<b>吴林晟</b>，邱良丰，毛军发"
				]
			},
			{
				"result":[
					"42",
					"ZD3017721",
					"A planar filtering crossover for three intersecting channels",
					"会议论文",
					"<b>Wu, Lin-Sheng</b>(#)(*)，Mao, Jun-Fa"
				]
			},
			{
				"result":[
					"43",
					"ZD3222787",
					"可重构功率分配器研究",
					"人才培养",
					""
				]
			},
			{
				"result":[
					"44",
					"ZD3035324",
					"基于交叉耦合抑制通道间互耦的滤波天线的实现方法",
					"专利",
					"<b>吴林晟</b>(#)(*)，毛军发"
				]
			},
			{
				"result":[
					"45",
					"ZD3114428",
					"一种抑制高速电路地弹噪声的超宽带平面电磁带隙结构",
					"专利",
					"李晓春(#)(*)，张佶，毛军发"
				]
			},
			{
				"result":[
					"46",
					"ZD3035273",
					"基于公度传输线网络的双通带滤波器",
					"专利",
					"<b>吴林晟</b>(#)(*)，张仕强，汤宇伟，毛军发"
				]
			},
			{
				"result":[
					"47",
					"ZD3112719",
					"共形双频段收发天线",
					"专利",
					"沈广海(#)，李静，彭宏利(*)，<b>吴林晟</b>"
				]
			},
			{
				"result":[
					"48",
					"ZD3035396",
					"具有稳定插入损耗的电可调负群时延电路",
					"专利",
					"<b>吴林晟</b>(#)(*)，邱良丰，毛军发"
				]
			},
			{
				"result":[
					"49",
					"ZD3114082",
					"基片集成同轴波导互连阵列结构",
					"专利",
					"李晓春(#)(*)，邵妍，王宁，袁斌，毛军发"
				]
			}
		],
		"supportNum":"78"
	},
	"message":"Success"
}

try:
	print(jmespath.search("code",ast.literal_eval(my)))
	kg = jmespath.search("data.downloadHref",ast.literal_eval(my))
	print(kg)
	print(type(str(jmespath.search("data.resultsList[]",ast.literal_eval(my)))))
	s = str(jmespath.search("data.resultsList[]",nomal))
	print(s)
	print(jmespath.search("data.ratifyNo", ast.literal_eval(my)))
except Exception as e:
	print(str(e))
