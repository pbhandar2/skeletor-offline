# skeletor-offline

A framework for analysis of block I/O traces. Configure the trace_config.json to tell the framework about the format of the trace. The framework will extract the necessary information and give you the metrics of the workload. 

Sample output implemented currently. 

{
    "autocorrelation": {
        "read_count": [
            1.0,
            0.0757017710006346,
            -0.006884969750605922,
            -0.006954540352187281,
            -0.008316230430040402,
            -0.010128494368791681,
            -0.009156389940666235,
            -0.004381790755729088,
            -0.012382180753461881,
            -0.013049183660691003,
            -0.012954672222960274,
            0.12583047181234527,
            0.0009746365140548911,
            -0.011319130249171024,
            -0.007031750153072291,
            -0.008413135447088136,
            -0.014425262648926495,
            -0.009795378590638722,
            0.036175909814614965,
            -0.011983770718608108,
            -0.016981197230233183,
            -0.01752531527043885,
            -0.018278116475056616,
            -0.019577396932837773,
            -0.020453858346282945,
            -0.021097830942823834,
            -0.022189486641270424,
            -0.021532160257629752,
            -0.022158759962702734,
            -0.02298735987774201,
            -0.023645301080290712,
            -0.02372367595802122,
            -0.02226766998836267,
            -0.02560933273614508,
            -0.022617108034897502,
            -0.02342165037840781,
            -0.022871855439144863,
            -0.024888733188096174,
            -0.02587743531232333,
            -0.026691462822339685,
            -0.027492069910654802
        ],
        "total_io": [
            1.0,
            0.06835559584205043,
            -0.008489066780113217,
            -0.010318161572830161,
            -0.013592062224809142,
            -0.017559892352752692,
            -0.013026890645092354,
            0.004072855710840927,
            -0.018962634121359723,
            -0.019453160236845072,
            -0.016466951391944245,
            0.13918987908120542,
            -0.003161306057472842,
            -0.013315737564733388,
            -0.0032112483167178203,
            -0.01333204917878653,
            -0.02155676011596714,
            -0.010719438387667316,
            0.11892667975773731,
            -0.009985165501754321,
            -0.019377169056762927,
            -0.020254718317567876,
            -0.022602389583170814,
            -0.0252498305326398,
            -0.020982524228415088,
            -0.024360819187403522,
            -0.025070260579051963,
            -0.023575040856806773,
            -0.02405321160344154,
            -0.024658561295307073,
            -0.02681838956014562,
            -0.026641386161824453,
            -0.01935021841991079,
            -0.026412011332560895,
            -0.02497559540405397,
            -0.024629829697686217,
            -0.020798658814398373,
            -0.02586525258231177,
            -0.025912604780092687,
            -0.029945826496080748,
            -0.028495073897553312
        ],
        "total_io_size": [
            1.0,
            0.04418098952611924,
            -0.004490490928435113,
            -0.005622195291065658,
            -0.006787223911984835,
            -0.00789266959795205,
            -0.007361948561652805,
            -0.004857125506197653,
            -0.009702832388319068,
            -0.010308366463880246,
            -0.00993752453933161,
            0.05049372388178788,
            -0.007120080975864023,
            -0.010187186036242352,
            -0.00781515564175977,
            -0.010931963936646213,
            -0.01368024910117435,
            -0.011243871730569087,
            0.05443322104533931,
            -0.01047765902274644,
            -0.014114341019693066,
            -0.014889817928619837,
            -0.015466041761116652,
            -0.01663123694194537,
            -0.016454615807567446,
            -0.017677563443614288,
            -0.01829135532053325,
            -0.017499859916107138,
            -0.018154303976552662,
            -0.018760782823650707,
            -0.019602657613547705,
            -0.019882511579187013,
            -0.018818734899012302,
            -0.02122051914355012,
            -0.020685882606023342,
            -0.02110422538408765,
            -0.020793872713837848,
            -0.02241875810309677,
            -0.022963172666986054,
            -0.024299222617643113,
            -0.024481468866750553
        ],
        "total_read_size": [
            1.0,
            0.048207526615818626,
            -0.002361682260351181,
            -0.003021932673984478,
            -0.003921660697217094,
            -0.004664036131722214,
            -0.00455557302000342,
            -0.005236273751312861,
            -0.006385449573768011,
            -0.006923832483277301,
            -0.007150422746045436,
            0.0333552819730857,
            -0.005176172147935513,
            -0.007892533198955835,
            -0.006147054554876457,
            -0.0077811956033047155,
            -0.010200673688146818,
            -0.008488216067794997,
            0.0013317858477869407,
            -0.01137343769048358,
            -0.012622500628554897,
            -0.01323198654634789,
            -0.013575530717122246,
            -0.014498152954383144,
            -0.015148389326866482,
            -0.015759078595099358,
            -0.016411887360778338,
            -0.01672359245267713,
            -0.01728991387907312,
            -0.017916175652500123,
            -0.01848595883570486,
            -0.018654346698551108,
            -0.01870319715099307,
            -0.02019340172544592,
            -0.01982959330120718,
            -0.02044156279767763,
            -0.020546553995306888,
            -0.02164890694093151,
            -0.02229879844201728,
            -0.022909991206085726,
            -0.02353731066649621
        ],
        "total_write_size": [
            1.0,
            -0.046686463210574895,
            -0.052011824208731135,
            -0.0513631590516385,
            -0.04154047579650299,
            -0.055234431812742214,
            -0.04745083189541601,
            0.2621163613112185,
            -0.05081569213590087,
            -0.06301806294467545,
            -0.0652422791542526,
            0.03233317614004134,
            -0.057008538634931355,
            -0.05423240541771852,
            -0.037013004327364714,
            -0.05471372089988121,
            -0.05381903153553408,
            -0.056212340627707975,
            0.21552399283279933,
            -0.0313014353664291,
            -0.01878583523565143,
            -0.02344395905221681,
            -0.02124470660187127,
            -0.029794243461851604,
            -0.02583376466895568,
            -0.025770783433902697,
            -0.01932246188868589,
            0.0018850829633862989,
            -0.002937512252561059,
            -0.0007229375640254568,
            -0.004197865536605026,
            -0.005635533665701473,
            -0.0007543041258932185,
            -0.0025702968647800754,
            0.003839207861217635,
            0.0038889933693552017,
            0.0048715923556943075,
            0.0014188317471231125,
            0.0013055015220016575,
            -0.0030041342601575187,
            -0.0018876830816565023
        ],
        "write_count": [
            1.0,
            -0.001022948930746042,
            -0.038951415153436,
            -0.03471984560480255,
            -0.009803945913765143,
            -0.06457761560939644,
            -0.025128168929103897,
            0.14162410361482464,
            -0.04732919568706278,
            -0.07608159472511851,
            -0.06187544204428509,
            0.0884028385438932,
            -0.0542828594621581,
            -0.05784262241733838,
            0.008073344835079741,
            -0.05575552396792871,
            -0.06384954590941297,
            -0.041862482174567846,
            0.4390604110252068,
            -0.022057022435256042,
            -0.025334135581058393,
            -0.0381878926528436,
            -0.034317489248375375,
            -0.05522349864234907,
            -0.030751658164307732,
            -0.04136932519593612,
            -0.019071180997085834,
            -0.015713406471911096,
            -0.021577944080600157,
            -0.01735758436863184,
            -0.023621834116911558,
            -0.024983090970491027,
            0.005398387483976103,
            -0.010158709409212317,
            -0.014929899372027168,
            -0.010961892174598017,
            0.005513304117730111,
            -0.012478075276681124,
            -0.007143902345435205,
            -0.025629714000638876,
            -0.015124771514630658
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
