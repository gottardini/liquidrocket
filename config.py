from collections import OrderedDict

jobfile="source/job.txt"
liquiddatafile="source/liquiddata.csv"
soliddatafile="source/soliddata.csv"
postprocfile="source/postproc.txt"


###ROCKETS SETTINGS
rockets=OrderedDict({
    "Ariane 5 ECA":[
        {
        'name':"Core stage",
        'index':0,
        'qty':1,
        'type':'liquid',
        'tStart':0,
        'tEnd':540,
        'zStart':0,
        'zEnd':157.7e3,
        },
        {
        'name':"Boosters",
        'index':0,
        'qty':2,
        'type':'solid',
        'tStart':0,
        'tEnd':140,
        'zStart':0,
        'zEnd':66.7e3,
        },
        {
        'name':"Second stage",
        'index':1,
        'qty':1,
        'type':'liquid',
        'tStart':540,
        'tEnd':1485,
        'zStart':157.7e3,
        'zEnd':250e3,
        },
    ],
    "Falcon Heavy":[
        {
        'name':"Core Stage",
        'index':2,
        'qty':9,
        'type':'liquid',
        'tStart':0,
        'tEnd':282,
        'zStart':0,
        'zEnd':92e3,
        },
        {
        'name':"Boosters",
        'index':2,
        'qty':18,
        'type':'liquid',
        'tStart':0,
        'tEnd':162,
        'zStart':0,
        'zEnd':62e3,
        },
        {
        'name':"Second Stage",
        'index':3,
        'qty':1,
        'type':'liquid',
        'tStart':282,
        'tEnd':679,
        'zStart':92e3,
        'zEnd':250e3,
        },
    ],
    "Saturn V":[
        {
        'name':"1st Stage",
        'index':4,
        'qty':5,
        'type':'liquid',
        'tStart':0,
        'tEnd':150.7,
        'zStart':0,
        'zEnd':65e3,
        },
        {
        'name':"2nd Stage",
        'index':5,
        'qty':5,
        'type':'liquid',
        'tStart':150.7,
        'tEnd':517.7,
        'zStart':65e3,
        'zEnd':175e3,
        },
        {
        'name':"3rd Stage - 1st burn",
        'index':6,
        'qty':1,
        'type':'liquid',
        'tStart':517.7,
        'tEnd':673.7,
        'zStart':175e3,
        'zEnd':185e3,
        },
        {
        'name':"3rd Stage - 2nd burn",
        'index':6,
        'qty':1,
        'type':'liquid',
        'tStart':673.7,
        'tEnd':1009.7,
        'zStart':185e3,
        'zEnd':250e3,
        },
    ],
})
