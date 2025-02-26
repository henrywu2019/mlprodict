
.. _l-HISTORY:

=======
History
=======

current - 2021-07-26 - 0.00Mb
=============================

* `289`: Avoids raising an exception when an optional parameter is not specified (2021-07-26)
* `287`: Adds python runtime for operator Loop, SequenceInsert, ConcatFromSequence (2021-07-25)
* `288`: Extends code coverage (2021-07-25)
* `286`: Adds runtime for operator Range (2021-07-13)

0.6.1447 - 2021-07-12 - 2.56Mb
==============================

* `285`: Adds function cst to create constant with numpy API for ONNX (2021-07-12)
* `283`: Commutative property (2021-07-12)
* `281`: Infers temporary allocation needed while computing the outputs (2021-07-12)
* `284`: Adds function transpose to numpy API for ONNX (2021-07-10)
* `282`: Upgrade requirements to skl2onnx>=1.9.0 (2021-07-02)
* `280`: More robustness for the python runtime (2021-07-01)
* `279`: Implements method infer_types in OnnxInference (2021-06-28)
* `278`: Adds operators ReduceSum, Max to OnnxMicroRuntime (2021-06-27)
* `277`: Switch to python 3.9 in CI (2021-06-25)
* `276`: Use openmp to parallelize QLinearConv (2021-06-25)
* `275`: Adds new strategy to pick up the best einsum equation based on ML (2021-06-25)
* `274`: Fixes issue raised with scipy 1.7.0 (2021-06-22)
* `273`: Adds operator where, improves numpy api (x[x<0]= 2) (2021-06-18)
* `272`: Explore custom implementation of operator add (2021-06-18)
* `271`: Updates default opset from 13 to 14 (2021-06-17)
* `270`: Adds more tests for QLinearConv runtime (2021-06-16)
* `269`: Adds runtime for operator QLinearConv (2021-06-04)
* `268`: Adds function to prepare data for onnxruntime_perf_test (2021-05-17)
* `267`: Moves onnxruntime code inside a wrapper to reduce logs (2021-05-14)
* `266`: Optimizes einsum even if not decomposed (2021-05-13)
* `265`: Refactoring, moves files to onnx_tools (2021-05-12)
* `264`: Support SessionOptions for runtime onnxruntime2 (2021-05-12)
* `263`: Refactor einsum files (2021-05-06)
* `262`: Refactoring, moving files into onnx_tools (2021-05-06)
* `261`: Improves einsum decomposition by using gemm and removing a transpose (2021-05-05)
* `260`: New command line to benchmark einsum decomposition (2021-05-03)
* `259`: Minor changes to Einsum decomposition (2021-05-02)
* `258`: Decomposes Einsum into simple matrix operations (2021-04-30)
* `257`: Fixes #256, add method to validate input data in numpy API for ONNX (2021-04-20)
* `256`: Add virtual method to validate input before predictions in numpy API for ONNX (2021-04-20)

0.5.1447 - 2021-04-17 - 0.38Mb
==============================

* `255`: Supports any embedded estimator with numpy API (2021-04-17)
* `254`: Adds python runtime for operator ReduceL1 (2021-04-16)
* `253`: Adds runtime for operator ReduceL2 (2021-04-14)
* `252`: Implements an experimental version of reducesum for the case RK (2021-04-07)
* `251`: Increases code coverage (2021-04-07)
* `250`: Increases code coverage of unit tests (2021-04-03)
* `248`: Adds implementation of BatchNormalization opset 14 (2021-03-29)
* `247`: Introduces FctVersion to fix issue with optional arguments (2021-03-29)
* `246`: Extends example on ReduceSum benchmark (2021-03-26)
* `244`: Supports embedded models, complete tutorial on numpy API for ONNX (2021-03-26)
* `243`: Add decorator to wrap converter for clustering (numpy API) (2021-03-17)
* `242`: Add decorator to wrap converter for classifier (numpy API) (2021-03-17)
* `241`: Add decorator to register scikit-learn classes with numpy API for ONNX (2021-03-14)
* `240`: Add decorator to wrap converter for regressor (numpy API) (2021-03-14)
* `239`: Add runtime empty (2021-03-13)
* `238`: Use numpy API for ONNX to write custom converters (2021-03-13)
* `237`: Add a unit test to check an exception (2021-03-10)
* `236`: Implements __setitem__ for one dimension array (2021-03-08)
* `235`: Supports profiling for runtime onnxruntime1 (2021-03-04)
* `233`: Extend documentation about numpy API for ONNX (2021-03-04)
* `234`: Add parameter overwrite to select_model_inputs_outputs (2021-03-03)
* `232`: Implements pickling for functions used in numpy API for ONNX (2021-03-03)
* `231`: Supports different inputs in select_model_inputs_outputs (2021-03-03)
* `230`: Add unsqueeze, squeeze, expand_dims to numpy API for ONNX (2021-03-02)
* `229`: Add method flatten, function pad to numpy API for ONNX (2021-03-01)
* `228`: Improves numpy API for ONNX: type constraints (2021-03-01)
* `227`: Add functions arange, cumsum, compress to numpy API for ONNX (2021-03-01)
* `226`: Add function Einsum to numpy API for ONNX (2021-02-28)
* `225`: Adds function Clip to numpy API for ONNX (2021-02-28)
* `224`: Adds functions ceil, round to numpy API for onnx (2021-02-27)
* `223`: Test numpy API against onnxruntime (2021-02-27)
* `222`: Add hyperbolic function, prod, mean, argmin, argmax (2021-02-26)
* `221`: Add many simple functions to numpy API for ONNX (2021-02-26)
* `220`: Tutorial on numpy API for ONNX (2021-02-26)
* `219`: Simplifies onnxfication of FunctionTransformer (2021-02-23)
* `218`: Implements __setitem__ for class OnnxVar (2021-02-21)
* `217`: Move custom operator to a specific method easier to maintain (2021-02-21)
* `216`: Fix crash with Gather, TopK when k=0 or indices is empty. (2021-02-20)
* `215`: Implements __getitem__ for OnnxVar (onnxnumpy) (2021-02-20)
* `214`: Implements numpy functions with onnx (2021-02-19)
* `213`: Add parameter show to plot_onnx. (2021-02-11)
* `212`: Fixes #210, check first models from zoo, fix operator conv when B is not null (2021-02-05)
* `210`: Investigate models from ONNX zoo (2021-02-05)
* `211`: numpy 1.20 does not allow nan values in int64 arrays any more, fix a unit test about imputer (2021-02-02)
* `208`: Add try catch around import in asv benchmark (2021-01-30)
* `207`: Reduces greater batch size to 10.000 instead of 100.000. (2021-01-29)
* `205`: Fixes asv configuration (2021-01-18)
* `206`: Build wheel for all many platforms in CI (2021-01-17)

0.5.1360 - 2021-01-04 - 0.35Mb
==============================

* `203`: Enable Python 3.9, enable opset 13, upgrade version number (2021-01-04)
* `202`: Enable opset 13 (ONNX) (2021-01-04)
* `201`: Fixes #200, add support for float16 (2020-12-30)
* `200`: Add support for bfloat16 (2020-12-30)
* `199`: Fix unit tests recently failing due to onnxruntime update. (2020-12-15)

0.4.1352 - 2020-12-11 - 1.42Mb
==============================

* `196`: Fixes operator Slice for opset 9 (2020-12-11)
* `198`: Fixes #197, add function to plot onnx graph with matplotlib (2020-12-09)
* `197`: Add a function to plot an onnx graph into matplotlib (2020-12-09)
* `195`: Fixes #194, add function to add an operator in the graph (2020-12-08)
* `194`: Add a function to insert a cast operator between two nodes (2020-12-08)
* `193`: Improves notebook coverage, update CI (2020-11-29)
* `192`: Fixes #191, improves performance of TreeEnsemble (2020-11-28)
* `191`: Improves performance of TreeEnsemble (2020-11-28)
* `190`: Fixes #189, parallelization of Einsum (2020-11-17)
* `189`: Introduce parallelization in experimental einsum implementation (2020-11-17)
* `188`: Fixes #187, custom implementation for operator Einsum (2020-11-15)
* `187`: Custom implementation for operator Einsum (2020-11-15)
* `186`: Fixes #185, add operator LessOrEqual (2020-11-15)
* `185`: Add operator LessOrEqual (2020-11-15)
* `181`: Fix converter xgboost when ntree_limit is set up (2020-11-14)
* `184`: Fixes #183, fix missing parameter black_op in OnnxPipeline (2020-11-07)
* `183`: Fix error in OnnxPipeline, parameter black_op not found (2020-11-07)
* `182`: Fixes #178, fix xgboost issue with ntree_limit (2020-11-07)
* `178`: Fixes unit test testing OnnxConv (issue with shapes) (2020-11-07)
* `180`: Fixes #179, fix guess_schema_from_data for categories (2020-11-03)
* `179`: guess_schema_data_type fails with category in dataframe (2020-11-03)
* `176`: Fixes #175, add operator dropout (2020-09-29)
* `175`: Add operator Dropout (2020-09-29)
* `174`: Add support for ReduceSum >= 13 (2020-09-21)
* `173`: Fixes #172, add runtime for operator MaxPool (2020-09-16)
* `172`: Add runtime for operator MaxPool (2020-09-16)
* `171`: Fixes #170, add operator Pad (2020-09-10)
* `170`: Add runtime for operator Pad (2020-09-10)

0.4.1259 - 2020-09-03 - 1.32Mb
==============================

* `169`: fix compiling issue with ubuntu 16.04 (2020-09-03)
* `167`: Add runtime for Operator Or (2020-08-25)
* `166`: Add runtime for operator And (2020-08-25)
* `165`: Add runtime for operator GreaterOrEqual (2020-08-25)
* `164`: Add runtime for operator If (2020-08-25)
* `163`: Add runtime for operator Unsqueeze (2020-08-25)
* `162`: Add runtime for operator Split (2020-08-25)
* `161`: Add support for disable_optimisation (2020-08-12)
* `160`: Fixes #159, add operator ConvTranspose, refactoring. (2020-08-07)
* `159`: Implements runtime for ConvTranspose (2020-08-07)
* `158`: Fixes benchmark import issues (2020-08-03)
* `157`: Simplify scenarios, reduce time for benchmark. (2020-08-02)
* `156`: Fixes #155, improves documentation (2020-08-02)
* `155`: Fixes API on documentation (2020-08-02)
* `154`: Fixes y_train dtype for most of the problems. Fixes subproblems with GridSearchCV (2020-07-31)
* `153`: Fixes #152, set set n_jobs to the number of CPU (2020-07-31)
* `152`: Set n_jobs to the number of core - 1 when doing benchmark (2020-07-31)
* `151`: Force operator Conv to use continuous array (2020-07-30)
* `150`: Fixes nan issue in operator conv (2020-07-29)
* `147`: Fixes #145, #150, shape inference for operator Conv (2020-07-29)
* `145`: Fixes missing shape inference for operator conv (2020-07-29)
* `149`: Fixes #148, add operator Atan (2020-07-22)
* `148`: Add operator atan (2020-07-22)
* `146`: Fixes #144, add operator GlobalAveragePool (2020-07-21)
* `144`: Implements operator GlobalAveragePool (2020-07-21)
* `143`: Fixes #142, add operator BatchNormalization (2020-07-21)
* `142`: Implement python runtime for operator BatchNormalization (2020-07-21)
* `141`: Fixes #140, add runtime for QuantizeLinear, DequantizeLinear (2020-07-20)
* `140`: Implement runtime for QuantizeLinear, DequantizeLinear (2020-07-20)

0.4.1204 - 2020-07-09 - 0.31Mb
==============================

* `139`: Add runtime for operator EyeLike (2020-07-08)
* `138`: Add code to register custom python operator (2020-07-08)
* `137`: Remove parameter dtype (onnx conversion) (2020-07-08)
* `136`: Add parameter reshape to OnnxTransformer (2020-07-03)
* `135`: Add a function to change the first dimension output (ONNX). (2020-07-03)
* `133`: Implements runtime for operator Gather (ONNX) (2020-06-18)
* `132`: Add operator StringNormalizer, Tokenizer, TfidfVectorizer (ONNX) (2020-06-15)
* `131`: Add custom operator solve (2020-06-12)
* `130`: Add operator Erf (ONNX) (2020-06-11)
* `129`: Add operator Einsum (ONNX) (2020-06-11)
* `128`: Fixes #127, implements OnnxPipeline, train, convert at each step (2020-06-08)
* `127`: Implements a pipeline which replaces early stages by onnx (2020-06-08)

0.3.1129 - 2020-06-04 - 0.29Mb
==============================

* `123`: Enables opset 12 (ONNX) (2020-06-04)
* `117`: Support for op_version in onnx grammar (2020-06-04)

0.3.1108 - 2020-05-20 - 0.29Mb
==============================

* `126`: Fix xgboost converter for xgboost >= 1.0 (2020-05-18)
* `125`: Refactor rewritten sklearn operators (2020-05-18)
* `124`: Fixes #122, capture standard C ouptput with dump_data_model, first step for #123 (2020-05-16)
* `122`: Captures C output when calling dump_data_and_model (2020-05-16)

0.3.1082 - 2020-05-01 - 2.84Mb
==============================

* `121`: Add function to convert array to bytes and bytes to array (onnx tensor) (2020-04-30)
* `120`: Fix discrepencies for SVM classifier (ONNX) (2020-04-30)
* `119`: Keep order in topk implementation (2020-04-17)
* `118`: opset is not propagated in OnnxTransformer (2020-04-09)

0.3.1070 - 2020-04-07 - 0.29Mb
==============================

* `115`: Add a function to replay a benchmark when this one was dumped (more accurate) (2020-04-06)
* `116`: Makes ZipMapDictionary picklable (2020-03-30)
* `114`: Add more parameters to specify benchmark time (2020-03-30)
* `113`: Add operators for opset 12 (2020-03-26)
* `112`: Number of feature is wrong for problem num-tr-clus (2020-03-20)

0.3.1029 - 2020-03-17 - 0.28Mb
==============================

* `111`: Reduce the number of allocation in TreeEnsemble when it is parallelized (cache) (2020-03-13)
* `110`: Implements runtime for operator Constant-12 (2020-03-06)
* `109`: Generate a benchmark with asv to compare different runtime. Update modules in asv. (2020-03-06)
* `108`: Add a function to reduce the memory footprint (2020-02-25)
* `106`: Add operator Neg (2020-02-25)
* `101`: Fix DecisionTreeClassifier disappearance on the benchmark graph (2020-02-25)
* `107`: Add operator IsNaN (2020-02-24)
* `105`: Support string labels for Linear, TreeEnsemble, SVM classifiers. (2020-02-24)
* `104`: Enable / disable parallelisation in topk (2020-02-23)
* `103`: Implements plot benchmark ratio depending on two parameters (2020-02-22)
* `102`: Fix conversion for xgboost 1.0 (2020-02-21)

0.3.975 - 2020-02-19 - 0.28Mb
=============================

* `100`: add notebook on TreeEnsemble (2020-02-19)
* `99`: Fixes #93, use same code for TreeEnsembleClassifier and TreeEnsembleRegression (2020-02-19)
* `93`: Use pointer for TreeClassifier (2020-02-19)
* `98`: mlprodict i broken after onnxruntime, skl2onnx update (2020-02-15)
* `97`: Add runtime for operator Conv (2020-01-24)
* `96`: Fixes #97, add runtime for operator Conv (2020-01-24)
* `95`: Fix OnnxInference where an output and an operator share the same name (2020-01-15)
* `94`: Raw scores are always positive for TreeEnsembleClassifier (binary) (2020-01-13)
* `90`: Implements a C++ runtime for topk (2019-12-17)
* `86`: Use pointers to replace treeindex in tree ensemble cpp runtime (2019-12-17)
* `92`: Implements a C++ version of  ArrayFeatureExtractor (2019-12-14)
* `89`: Implements a function which extracts some informations on the models (2019-12-14)
* `88`: Fix bug in runtime of GatherElements (2019-12-14)

0.3.853 - 2019-12-13 - 0.24Mb
=============================

* `87`: Add converter for HistGradientBoostRegressor (2019-12-09)
* `85`: Implements a precompiled run method in OnnxInference (runtime='python_compiled') (2019-12-07)
* `84`: Automatically creates files to profile time_predict function in the benchmark with py-spy (2019-12-04)
* `83`: ONNX: includes experimental operators in the benchmark (2019-12-04)
* `82`: Function translate_fct2onnx: use of opset_version (2019-12-04)
* `81`: ONNX benchmark: track_score returns scores equal to 0 or 1 (unexpected) (2019-12-04)
* `80`: ONNX: extend benchmark to decision_function for some models (2019-12-03)
* `77`: Improves ONNX benchmark to measure zipmap impact. (2019-12-03)
* `76`: Implements ArgMax 12, ArgMax 12 (python onnx runtime) (2019-11-27)
* `75`: ONNX: fix random_state whevever it is available when running benchmark (2019-11-27)

0.3.765 - 2019-11-21 - 0.22Mb
=============================

* `59`: ONNX: Investigate kmeans and opset availability. (2019-11-21)
* `66`: ONNX: improves speed of python runtime for decision trees (2019-11-19)
* `74`: Function _modify_dimension should return the same dataset if called the same parameter (even if it uses random functions) (2019-11-15)
* `73`: ONNX: fix links on benchmark page (opset is missing) (2019-11-07)
* `72`: ONNX: support of sparse tensor for a unary and binary python operators (2019-11-06)
* `71`: ONNX: add operator Constant (2019-11-06)
* `67`: ONNX: improves speed of svm regressor (2019-11-06)
* `70`: ONNX: write tools to test convervsion for models in scikit-learn examples (2019-10-29)
* `65`: ONNX: investigate discrepencies for k-NN (2019-10-28)
* `69`: ONNX: side by side should work by name and not by positions (2019-10-23)
* `68`: ONNX: improves speed of SGDClassifier (2019-10-23)
* `61`: Implements a function to create a benchmark based on asv (ONNX) (2019-10-17)
* `63`: Export asv results to csv (ONNX) + command line (2019-10-11)
* `64`: Add an example with lightgbm and categorical variables (ONNX) (2019-10-07)
* `62`: Implements command line for the asv benchmark (ONNX) (2019-10-04)
* `60`: Improve lightgbm converter (ONNX) (2019-09-30)
* `58`: Fix table checking model, merge is wrong in documentation (2019-09-20)

0.2.542 - 2019-09-15 - 0.59Mb
=============================

* `57`: ONNX: handles dataframe when converting a model (2019-09-15)
* `56`: ONNX: implements cdist operator (2019-09-12)
* `54`: ONNX: fix summary, it produces multiple row when model are different when opset is different (2019-09-12)
* `51`: ONNX: measure the time performance obtained by using optimization (2019-09-11)
* `52`: ONNC-cli: add a command line to optimize an onnx model (2019-09-10)
* `49`: ONNX optimization: remove redundant subparts of a graph (2019-09-09)
* `48`: ONNX optimization: reduce the number of Identity nodes (2019-09-09)
* `47`: Implements statistics on onnx graph and sklearn models, add them to the documentation (2019-09-06)
* `46`: Implements KNearestNeibhorsRegressor supporting batch mode (ONNX) (2019-08-31)
* `45`: KNearestNeighborsRegressor (2019-08-30)
* `44`: Add an example to look into the performance of every node for a particular dataset (2019-08-30)
* `43`: LGBMClassifier has wrong shape (2019-08-29)

0.2.452 - 2019-08-28 - 0.13Mb
=============================

* `42`: Adds a graph which visually summarize the validating benchmark (ONNX). (2019-08-27)
* `41`: Enables to test multiple number of features at the same time (ONNX) (2019-08-27)
* `40`: Add a parameter to change the number of featuress when validating a model (ONNX). (2019-08-26)
* `39`: Add a parameter to dump all models even if they don't produce errors when being validated (ONNX) (2019-08-26)
* `24`: support double for TreeEnsembleClassifier (python runtime ONNX) (2019-08-23)
* `38`: See issue on onnxmltools. https://github.com/onnx/onnxmltools/issues/321 (2019-08-19)
* `35`: Supports parameter time_kwargs in the command line (ONNX) (2019-08-09)
* `34`: Add intervals when measuring time ratios between scikit-learn and onnx (ONNX) (2019-08-09)
* `31`: Implements shape inference for the python runtime (ONNX) (2019-08-06)
* `15`: Tells operator if the execution can be done inplace for unary operators (ONNX). (2019-08-06)
* `27`: Bug fix (2019-08-02)
* `23`: support double for TreeEnsembleRegressor (python runtime ONNX) (2019-08-02)

0.2.363 - 2019-08-01 - 0.11Mb
=============================

* `26`: Tests all converters in separate processeses to make it easier to catch crashes (2019-08-01)
* `25`: Ensures operator clip returns an array of the same type (ONNX Python Runtime) (2019-07-30)
* `22`: Implements a function to shake an ONNX model and test float32 conversion (2019-07-28)
* `21`: Add customized converters (2019-07-28)
* `20`: Enables support for TreeEnsemble operators in python runtime (ONNX). (2019-07-28)
* `19`: Enables support for SVM operators in python runtime (ONNX). (2019-07-28)
* `16`: fix documentation, visual graph are not being rendered in notebooks (2019-07-23)
* `18`: implements python runtime for SVM (2019-07-20)
* `17`: add a mechanism to use ONNX with double computation (2019-07-15)
* `13`: add automated benchmark of every scikit-learn operator in the documentation (2019-07-05)
* `12`: implements a way to measure time for each node of the ONNX graph (2019-07-05)
* `11`: implements a better ZipMap node based on dedicated container (2019-07-05)
* `8`: implements runtime for decision tree (2019-07-05)
* `7`: implement python runtime for scaler, pca, knn, kmeans (2019-07-05)
* `10`: implements full runtime with onnxruntime not node by node (2019-06-16)
* `9`: implements a onnxruntime runtime (2019-06-16)
* `6`: first draft of a python runtime for onnx (2019-06-15)
* `5`: change style highlight-ipython3 (2018-01-05)
