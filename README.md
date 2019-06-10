# skeletor-offline

A framework for analysis of block I/O traces. Configure the trace_config.json to tell the framework about the format of the trace. The framework will extract the necessary information and give you the metrics of the workload. 

Sample output implemented currently. 

{
    "autocorrelation": {  
        "read_count": [  
        	...  
        ],
        "total_io": [
        	...  
        ],
        "total_io_size": [
        	...  
        ],
        "total_read_size": [
        	...  
        ],
        "total_write_size": [
        	...  
        ],
        "write_count": [
        	...  
        ]
    },
    "average_io_size": 24995.4048,
    "average_read_size": 34627.571556219846,
    "average_write_size": 9574.467916872578,
    "fano": {
        "read_count": 33993.036296432416,
        "total_io": 24785.474239929994,
        "total_io_size": 1410791581.5153537,
        "total_read_size": 1594434247.1720614,
        "total_write_size": 34999707.83431738,
        "write_count": 909.4827720999155
    },
    "io_rate": 7.236821383434507,
    "max_read_size": 888832,
    "max_write_size": 65536,
    "min_read_size": 512,
    "min_write_size": 512,
    "moments": {
        "read_count": {
            "kurtosis": 38.22202949697676,
            "skewness": 6.252321543724882,
            "variance": 46472257.621256046
        },
        "total_io": {
            "kurtosis": 36.42599182069314,
            "skewness": 6.0575551441702755,
            "variance": 54958759.791304335
        },
        "total_io_size": {
            "kurtosis": 39.88509697816722,
            "skewness": 6.43101638522225,
            "variance": 7.831293484919774e+16
        },
        "total_read_size": {
            "kurtosis": 40.40654389940964,
            "skewness": 6.489879550571064,
            "variance": 7.550433314831605e+16
        },
        "total_write_size": {
            "kurtosis": 26.422866714195163,
            "skewness": 5.068954144814966,
            "variance": 285422200503449.3
        },
        "write_count": {
            "kurtosis": 15.75485588693401,
            "skewness": 4.056957247443964,
            "variance": 773302.8850241547
        }
    },
    "read_count": 61553,
    "read_rate": 4.454480666145442,
    "read_write_ratio": 1.6009831716388796,
    "total_io": 100000,
    "total_io_size": 2499540480,
    "total_read_size": 2131430912,
    "total_write_size": 368109568,
    "write_count": 38447,
    "write_rate": 2.782340717289065
}
