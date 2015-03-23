# encoding:utf-8
__author__ = 'Mark-Fighting'
import re

a = ["1","2"]
print ''.join(a)

a = '''<div id="sina_keyword_ad_area2" class="articalContent   newfont_family">
			<div><font STYLE="font-size: 16px;"><b>　　【物流：外运发展、新宁物流、长江投资、中储股份、华贸物流、铁龙物流、澳洋顺昌】</B></FONT></DIV>
<div><font STYLE="font-size: 16px;">　　涨停原因揭秘：国务院日前印发《关于同意设立中国(杭州)跨境电子商务综合试验区的批复》，杭州创建跨境电商综合试验区，有利于主动应对全球贸易新格局，相关物流企业将从中获益。受此影响，相关个股涨停，外运发展（600270）主营国际货运代理业务及相关报关业务。</FONT></DIV>
<div><font STYLE="font-size: 16px;">　　新宁物流（300013）主营采购与生产环节提供第三方综合物流服务。长江投资（600119）的物流业营收占总营收的68.03%。中储股份（600787）主营商品储存、物资配送、货运代理等。</FONT></DIV>
<div><font STYLE="font-size: 16px;">　　华贸物流（603128）主营现代物流业。铁龙物流（600125）主营铁路特种集装箱、铁路货运及临港物流业务。澳洋顺昌（002245）主营钢板、铝板物流配送。</FONT></DIV>
<div><font STYLE="font-size: 16px;"><br /></FONT></DIV>
<div><font STYLE="font-size: 16px;"><b>　　【互联网+：生意宝、腾邦国际、二三四五、天成控股】</B></FONT></DIV>
<div><font STYLE="font-size: 16px;">　　涨停原因揭秘：3月15日，李克强总理在记者会上强调，网上网下互动创造的是活力，是更大的空间，站在“互联网+”的风口上顺势而为，会使中国经济飞起来。受此影响，今日互联网金融概念股纷纷涨停。生意宝子公司主营非金融机构互联网支付业务。</FONT></DIV>
<div><font STYLE="font-size: 16px;">　　腾邦国际（300178）子公司主营P2P网贷业务。二三四五（002195）拟设子公司主营互联网金融业务。天成控股（600112）拟投1.5亿完成互联网支付、移动支付等全国性业务平台的建立。</FONT></DIV>
<div><font STYLE="font-size: 16px;"><br /></FONT></DIV>
<div><font STYLE="font-size: 16px;"><b>　　【网络安全：长城电脑、蓝盾股份、立思辰】</B></FONT></DIV>
<div><font STYLE="font-size: 16px;">　　涨停原因揭秘：央视在315晚会现场表示，黑客利用免费WiFi网络窃取用户的邮箱账号和密码，从而窃取个人更多隐私信息的风险，网络安全问题再次成为热点。受此影响，相关个股涨停，长城电脑（000066）将投资8214万元建信息安全研发中心。</FONT></DIV>
<div><font STYLE="font-size: 16px;">　　蓝盾股份（300297）主营企业级信息安全产品的研发、生产及销售。立思辰（300010）子公司拥有国家保密局颁发的涉及国家秘密的计算机信息系统集成资质证书。</FONT></DIV>
<div><font STYLE="font-size: 16px;"><br /></FONT></DIV>
<div><font STYLE="font-size: 16px;"><b>　　【高送转：安硕信息、数字政通、新世纪】</B></FONT></DIV>
<div><font STYLE="font-size: 16px;">　　涨停原因揭秘：进入新的一年，已发布高送转预案个股的权益分派日纷纷到来，高送转抢权行情悄然启动，高送转概念股今日纷纷涨停。安硕信息（300380）10转10派2元。数字政通（300075）拟10转10派1元。新世纪（002280）拟10转15派2元。</FONT></DIV>
<div><font STYLE="font-size: 16px;"><br /></FONT></DIV>
<div><font STYLE="font-size: 16px;"><b>　　【次新股：博世科、晨光文具、仙坛股份、龙马环卫、东兴证券、火炬电子】</B></FONT></DIV>
<div><font STYLE="font-size: 16px;">　　涨停原因揭秘：随着注册制日益临近，上市新股越加受到资金追捧。注册制下的上市新股能否像审核制下一样遭到爆炒，仍需时间验证。因此在审核制下，市场资金越加珍惜对最后这几批上市新股的炒作。受此影响，今日博世科（300422）等6只次新股涨停。</FONT></DIV>
<div><font STYLE="font-size: 16px;"><br /></FONT></DIV>
<div><font STYLE="font-size: 16px;"><b>　　【并购重组：法因数控、安彩高科、启明星辰、喜临门、恒信移动、湖北金环、桑乐金、山东如意、洪涛股份、正邦科技】</B></FONT></DIV>
<div><font STYLE="font-size: 16px;">　　涨停原因揭秘：法因数控（002270）拟以非公开发行股份的方式收购上海华明100%股权，交易作价26亿元。上海华明主营变压器有载分接开关和无励磁分接开关以及其它输变电设备的研发、制造、销售和服务。</FONT></DIV>
<div><font STYLE="font-size: 16px;">　　安彩高科（600207）拟以不低于4.75元/股的价格，非公开发行股份不超过1.44亿股，募资不超过6.85亿元，资金将用于收购中原天然气55%股权、补充流动资金。</FONT></DIV>
<div><font STYLE="font-size: 16px;">　　启明星辰（002439）拟以发行股份及支付现金相结合的方式购买安方高科100%股权，并以发行股份的方式购买控股子公司合众数据49%股权，交易总价3.76亿元。</FONT></DIV>
<div><font STYLE="font-size: 16px;">　　喜临门（603008）拟以7.2亿元的价格收购绿城传媒100%股权。绿城传媒主营电视剧的投资、制作、发行及衍生业务。</FONT></DIV>
<div><font STYLE="font-size: 16px;">　　恒信移动（300081）拟以发行股份方式收购易视腾91.30%股权，交易对价不超过8.21亿元。易视腾主营互联网电视核心技术研发、智能终端开发及销售、OTT业务运营服务。</FONT></DIV>
<div><font STYLE="font-size: 16px;">　　湖北金环（000615）拟发行股份及支付现金购买京汉置业全体股东持有的京汉置业全部股权，交易作价14.95亿元。京汉置业主营房地产开发业务，拥有国家房地产开发一级资质。</FONT></DIV>
<div><font STYLE="font-size: 16px;">　　桑乐金（300247）拟以9.79元/股的价格，非公开发行股份6300万股并支付现金的方式购买久工健业100%股权，交易作价8.1亿元。久工健业主营健康按摩器具的研发、生产及销售。</FONT></DIV>
<div><font STYLE="font-size: 16px;">　　山东如意（002193）拟以不低于9.14元/股的价格，非公开发行股份不超过2.3亿股，募集资金不超过20.01亿元，资金将用于收购泰安如意100%股权、温州庄吉51%股权、建设如意纺高档精纺面料项目、科研项目、如意纺200万套高档西装项目、偿还银行贷款。</FONT></DIV>
<div><font STYLE="font-size: 16px;">　　洪涛股份（002325）与北京尚学跨考教育科技有限公司及其原股东共同签署《股权转让及增资协议》，公司以2.35亿元的对价取得跨考教育70%股权。跨考教育主营考研培训。</FONT></DIV>
<div><font STYLE="font-size: 16px;">　　正邦科技（002157）全资子公司正邦(香港)贸易拟以现金方式购买江西正邦生物化工有限责任公司100%股权，交易作价6.2亿元。正邦生化主营农药制剂的研发、生产和销售及提供专业植保技术服务。</FONT></DIV>
<div><font STYLE="font-size: 16px;"><br /></FONT></DIV>
<div><font STYLE="font-size: 16px;"><b>　　【定增募资：广电运通、二六三、山鹰纸业】</B></FONT></DIV>
<div><font STYLE="font-size: 16px;">　　涨停原因揭秘：广电运通（002152）拟以17.76元/股的价格，非公开发行股份不超过2.1亿股，募集资金不超过37.29亿元，资金拟用于建设全国金融外包服务平台以及补充流动资金。</FONT></DIV>
<div><font STYLE="font-size: 16px;">　　二六三（002467）拟以不低于15.47元/股的价格，非公开发行股份不超过5068万股，募集资金不超过7.84亿元，资金拟用于全球华人移动通信服务项目及企业云统一通信服务项目。</FONT></DIV>
<div><font STYLE="font-size: 16px;">　　山鹰纸业（600567）拟不低于2.48
元/股的价格，非公开发行股份不超过8.07亿股，募集资金不超过20亿元，资金将用于低定量强韧牛卡纸、低定量高强瓦楞纸、渣浆纱管原纸生产线建设项目。</FONT></DIV>
<div><font STYLE="font-size: 16px;"><b><br /></B></FONT></DIV>
<div><font STYLE="font-size: 16px;"><b>　　【在线教育：新南洋、东方创业】</B></FONT></DIV>
<div><font STYLE="font-size: 16px;">　　涨停原因揭秘：新南洋（600661）拟出资1.3亿元、东方创业（600278）拟出资1.5亿元，与上海交大产业投资管理(集团)有限公司、上海赛领股权投资基金合伙企业及上海创旗投资管理中心(有限合伙)共同发起设立教育产业投资基金上海交大赛领创业教育股权投资基金，基金总规模10.05亿，掘金K12(基础教育)、互联网教育等领域。</FONT></DIV>
<div><font STYLE="font-size: 16px;"><br /></FONT></DIV>
<div><font STYLE="font-size: 16px;"><b>　　【航空航运：南方航空、中昌海运】</B></FONT></DIV>
<div><font STYLE="font-size: 16px;">　　涨停原因揭秘：在市场持续担心美国库存持续增加之际，美元陡然走强，令持续低迷的原油市场遭受更大打击。近日油价持续下跌，创2月26日以来最低收盘位。油价下降，经营成本中燃油比例较大航空航运业将受益，今日南方航空（600029）、中昌海运（600242）涨停。</FONT></DIV>
<div><font STYLE="font-size: 16px;"><br /></FONT></DIV>
<div><font STYLE="font-size: 16px;"><b>　　【光伏：向日葵】</B></FONT></DIV>
<div><font STYLE="font-size: 16px;">　　涨停原因揭秘：向日葵（300111）拟非公开发行股份4亿股，募集资金12.5亿元，资金将用于120MW分布式光伏并网发电项目和补充公司流动资金。</FONT></DIV>
<div><font STYLE="font-size: 16px;"><br /></FONT></DIV>
<div><font STYLE="font-size: 16px;"><b>　　【金融IC卡：易联众】</B></FONT></DIV>
<div><font STYLE="font-size: 16px;">　　涨停原因揭秘：昨日政府开始实施要求商业银行采购“安全可控”IT设备的新规，要求银行IT供货商在中国开展研发、并向银监会提交源代码。这可能与其欧盟、美国发生冲突，国产金融IT设备企业有望受益。受此影响，掌握有社保IC卡金融应用功能核心技术的易联众（300096）今日涨停。</FONT></DIV>
		</div>
						<!-- 正文结束 -->
		<div id='share' class="shareUp">
		</div>
						<!-- 正文结束 -->'''
divPattern = r'''id="sina_keyword_ad_area2"([\s\S]*?)id='share'''
reg = re.compile(divPattern)
m = reg.findall(a)
print m


r = re.compile("href=['\"]http://.+?['\"]")
res_info = '''href="http://blog.sina.com.cn/s/blog_a6534c720102vede.html?"aaaa"href="http://blog.sina.com.cn/s/blog_a64c720102vede.html?"'''
m = r.findall(a)

regex_tag = {
    re.compile(r"href=['\"]http://.+?['\"]"): "",
    re.compile(r"target=['\"].+?['\"]"): "",
    re.compile(r"class=['\"].+?['\"]"): "",
}

for k,v in regex_tag.iteritems():
    f_tmp = k.findall(res_info)
    for item in f_tmp:
        res_info = res_info.replace(item,v)

print res_info


b = "aaabcd"
print b.rfind("c")