jobfile="source/job.txt"
datafile="source/data.csv"
postprocfile="source/postproc.txt"


###ROCKETS SETTINGS
rockets={
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
        'index':2,
        'qty':2,
        'type':'solid',
        'tStart':0,
        'tEnd':140,
        'zStart':0,
        'zEnd':66.7e3,
        },
    ]
}
