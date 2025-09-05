from ._mapi import *
#--------------------------------------------------------------------------------------------------

class AnalysisControl:
    
    class MainControlData:
        
        data = []
        
        def __init__(self, 
                    ardc: bool = True,
                    anrc: bool = True,
                    iter: int = 20,
                    tol: float = 0.001,
                    csecf: bool = False,
                    trs: bool = True,
                    crbar: bool = False,
                    bmstress: bool = False,
                    clats: bool = False):
            """
            Main Control Data constructor for analysis control settings.
            
            Parameters:
                ardc: Auto Rotational DOF Constraint for Truss/Plane Stress/Solid Elements (default True)
                
                anrc: Auto Normal Rotation Constraint for Plate Elements (default True)

                iter: Number of Iterations/Load Case (default 20)

                tol: Convergence Tolerance (default 0.001)
                
                csecf: Consider Section Stiffness Scale Factor for Stress Calculation (default False)

                trs: Transfer Reactions of Slave Node to the Master Node (default True)

                crbar: Consider Reinforcement for Section Stiffness Calculation (default False)

                bmstress: Calculate Equivalent Beam Stresses (Von-Mises and Max-Shear) (default False)
                
                clats: Change Local Axis of Tapered Section for Force/Stress Calculation (default False)
            
            Examples:
                # Basic control data with required parameters
                MainControlData(iter=20, tol=0.001)
                
                # with multiple options enabled
                MainControlData(
                    ardc=True, anrc=True, iter=30, tol=0.0005,
                    trs=True, bmstress=True
                )
            """
            
            # Validate required parameters
            if iter is None:
                raise ValueError("iter (Number of Iterations) is required")
            if tol is None:
                raise ValueError("tol (Convergence Tolerance) is required")
            
            # ID is always 1
            self.ID = 1
            
            # Set parameters
            self.ARDC = ardc
            self.ANRC = anrc
            self.ITER = iter
            self.TOL = tol
            self.CSECF = csecf
            self.TRS = trs
            self.CRBAR = crbar
            self.BMSTRESS = bmstress
            self.CLATS = clats
            
            # Add to static list
            AnalysisControl.MainControlData.data.append(self)
            
            # Automatically execute the data when instance is created
            self._execute()
        
        def _execute(self):
            """
            Automatically sends the MainControlData to the analysis system when created
            """
            json_data = {"Assign": {}}
            
            control_data = {
                "ARDC": self.ARDC,
                "ANRC": self.ANRC,
                "ITER": self.ITER,
                "TOL": self.TOL,
                "CSECF": self.CSECF,
                "TRS": self.TRS,
                "CRBAR": self.CRBAR,
                "BMSTRESS": self.BMSTRESS,
                "CLATS": self.CLATS
            }
            
            json_data["Assign"][str(self.ID)] = control_data
            
            MidasAPI("PUT", "/db/actl", json_data)

    class PDelta:
        """Create P-Delta Analysis Control Object in Python"""
        data = []
        
        def __init__(self, 
                    iter: int = 5,
                    tol: float = 0.00001,
                    load_case_data: list = None):
            """
            P-Delta Analysis Control constructor for geometric nonlinear analysis settings.
            
            Parameters:
                iter: Number of Iterations (default 5)
                
                tol: Convergence Tolerance (default 0.00001)

                load_case_data: Load Cases with Scale Factors (required)
                    - List of load cases and their corresponding scale factors for P-Delta analysis
                    - Format: [["LC1", factor1], ["LC2", factor2], ...]

            Example:
        
                PDelta(iter=5, load_case_data=[["DL", 1.0]])   
    
            """
            
            # Validate required parameters
            if iter is None:
                raise ValueError("iter (Number of Iterations) is required")
            if load_case_data is None or len(load_case_data) == 0:
                raise ValueError("load_case_data (Load Cases) is required")
            
            # Validate load case data format
            for i, case in enumerate(load_case_data):
                if not isinstance(case, list) or len(case) != 2:
                    raise ValueError(f"load_case_data[{i}] must be a list with 2 elements [name, factor]")
                if not isinstance(case[0], str):
                    raise ValueError(f"load_case_data[{i}][0] (load case name) must be a string")
                if not isinstance(case[1], (int, float)):
                    raise ValueError(f"load_case_data[{i}][1] (scale factor) must be a number")
            
            # ID is always 1
            self.ID = 1
            
            # Set parameters
            self.ITER = iter
            self.TOL = tol
            self.LOAD_CASE_DATA = load_case_data
            
            # Add to static list
            AnalysisControl.PDelta.data.append(self)
            
            # Automatically execute the data when instance is created
            self._execute()
        
        def _execute(self):
            """
            Automatically sends the P-Delta Analysis Control to the analysis system when created
            """
            json_data = {"Assign": {}}
            
            # Convert load case data to required format
            pdel_cases = []
            for case_name, factor in self.LOAD_CASE_DATA:
                pdel_cases.append({
                    "LCNAME": case_name,
                    "FACTOR": factor
                })
            
            control_data = {
                "ITER": self.ITER,
                "TOL": self.TOL,
                "PDEL_CASES": pdel_cases
            }
            
            json_data["Assign"][str(self.ID)] = control_data
            
            MidasAPI("PUT", "/db/pdel", json_data)

    class Buckling:
            """Create Buckling Analysis Control Object in Python"""
            data = []
            
            def __init__(self, 
                        mode_num: int = None,
                        opt_positive: bool = True,
                        load_factor_from: float = 0,
                        load_factor_to: float = 0,
                        opt_sturm_seq: bool = False,
                        opt_consider_axial_only: bool = False,
                        load_case_data: list = None):
                """
                Buckling Analysis Control constructor for eigenvalue buckling analysis settings.
                
                Parameters:
                    mode_num: Number of Modes (required)
                    
                    opt_positive: Load Factor Range Type (default True)
                    
                    load_factor_from: Search From (default 0)
                        - Lower bound for load factor search range
                        - Only used when opt_positive is False (Search mode)

                    load_factor_to: Search To (default 0)
                        - Upper bound for load factor search range
                        - Only used when opt_positive is False (Search mode)

                    opt_sturm_seq: Check Sturm Sequence (default False)
                    
                    opt_consider_axial_only: Frame Geometric Stiffness Option (default False)
                    
                    load_case_data: Load Cases with Scale Factors and Types (required)
                        - List of load cases with their scale factors and load types
                        - Format: [["LC1", factor1, load_type1], ["LC2", factor2, load_type2], ...]
                        - Load case name (string), scale factor (number), load type (integer)
                        - Load Type: 0=Variable, 1=Constant
                
                
                Examples:
                    Buckling(
                        mode_num=8, opt_positive=False, 
                        load_factor_from=-2.0, load_factor_to=5.0,
                        opt_consider_axial_only=True,
                        load_case_data=[["Gravity", 1.0, 1], ["Lateral", 1.0, 0]]
                    )
                """
                
                # Validate required parameters
                if mode_num is None:
                    raise ValueError("mode_num (Number of Modes) is required")
                if load_case_data is None or len(load_case_data) == 0:
                    raise ValueError("load_case_data (Load Cases) is required")
                
                # Validate load case data format
                for i, case in enumerate(load_case_data):
                    if not isinstance(case, list) or len(case) != 3:
                        raise ValueError(f"load_case_data[{i}] must be a list with 3 elements [name, factor, load_type]")
                    if not isinstance(case[0], str):
                        raise ValueError(f"load_case_data[{i}][0] (load case name) must be a string")
                    if not isinstance(case[1], (int, float)):
                        raise ValueError(f"load_case_data[{i}][1] (scale factor) must be a number")
                    if not isinstance(case[2], int) or case[2] not in [0, 1]:
                        raise ValueError(f"load_case_data[{i}][2] (load type) must be 0 (Variable) or 1 (Constant)")
                
                # ID is always 1
                self.ID = 1
                
                # Set parameters
                self.MODE_NUM = mode_num
                self.OPT_POSITIVE = opt_positive
                self.LOAD_FACTOR_FROM = load_factor_from
                self.LOAD_FACTOR_TO = load_factor_to
                self.OPT_STURM_SEQ = opt_sturm_seq
                self.OPT_CONSIDER_AXIAL_ONLY = opt_consider_axial_only
                self.LOAD_CASE_DATA = load_case_data
                
                # Add to static list
                AnalysisControl.Buckling.data.append(self)
                
                # Automatically execute the data when instance is created
                self._execute()
            
            def _execute(self):
                """
                Automatically sends the Buckling Analysis Control to the analysis system when created
                """
                json_data = {"Assign": {}}
                
                # Convert load case data to required format
                items = []
                for case_name, factor, load_type in self.LOAD_CASE_DATA:
                    items.append({
                        "LCNAME": case_name,
                        "FACTOR": factor,
                        "LOAD_TYPE": load_type
                    })
                
                control_data = {
                    "MODE_NUM": self.MODE_NUM,
                    "OPT_POSITIVE": self.OPT_POSITIVE,
                    "OPT_CONSIDER_AXIAL_ONLY": self.OPT_CONSIDER_AXIAL_ONLY,
                    "LOAD_FACTOR_FROM": self.LOAD_FACTOR_FROM,
                    "LOAD_FACTOR_TO": self.LOAD_FACTOR_TO,
                    "OPT_STURM_SEQ": self.OPT_STURM_SEQ,
                    "ITEMS": items
                }
                
                json_data["Assign"][str(self.ID)] = control_data
                
                MidasAPI("PUT", "/db/buck", json_data)


    class EigenValue:
        """Create Eigen Vector Analysis Control Object in Python"""
        data = []
        
        def __init__(self, 
                    analysis_type: str = None,
                    # EIGEN specific parameters
                    ifreq: int = 1,
                    iiter: int = 20,
                    idim: int = 1,
                    tol: float = 0,
                    # LANCZOS specific parameters 
                    frequency_range: list = None,  
                    bstrum: bool = False,
                    bminmax: bool = None,
                    frmin: float = None,
                    frmax: float = None,
                    # RITZ specific parameters 
                    bincnl: bool = False,
                    ignum: int = None,
                    load_vector: list = None,  
                    vritz: list = None):
            """
            Eigen Vector Analysis Control 
            
            Parameters:
                analysis_type: Type of Analysis (required)
                    - "EIGEN": Subspace Iteration
                    - "LANCZOS": Lanczos
                    - "RITZ": Ritz Vectors
                
                # For EIGEN:
                ifreq: Number of Frequencies (required for EIGEN)
                iiter: Number of Iterations (required for EIGEN)
                idim: Subspace Dimension (default 0, optional for EIGEN)
                tol: Convergence Tolerance (default 0, optional for EIGEN)
                
                # For LANCZOS :
                frequency_range: Frequency Range [frmin, frmax] (optional for LANCZOS)
                    - If provided, automatically sets bMINMAX=True
                    - Format: [min_freq, max_freq]
                bstrum: Sturm Sequence Check (default False, optional for LANCZOS)
                
                # For RITZ type only:
                bincnl: Include GL-link Force Vectors (default False, optional for RITZ)
                ignum: Number of Generations for Each GL-link Force (required for RITZ)
                load_vector: Load Cases in simple format (required for RITZ)
                    - Format: [["case_or_acc", nog], ...]
                    - For ground acceleration: ["ACCX"/"ACCY"/"ACCZ", nog]
                    - For load case: ["case_name", nog]
            
            Examples:
                # EIGEN analysis
                EigenValue(
                    analysis_type="EIGEN",
                    ifreq=10,
                    iiter=20,
                    idim=1,
                    tol=1e-10
                )
                
                # LANCZOS analysis
                EigenValue(
                    analysis_type="LANCZOS",
                    ifreq=15,
                    frequency_range=[0, 1600],  # Automatically sets bMINMAX=True
                    bstrum=True
                )
                
                # RITZ analysis
                EigenValue(
                    analysis_type="RITZ",
                    bincnl=False,
                    ignum=1,
                    load_vector=[["DL", 1], ["ACCX", 1]]  # Simple format
                )
            """
            
            # Validate required parameters
            if analysis_type is None:
                raise ValueError("analysis_type is required")
            if analysis_type not in ["EIGEN", "LANCZOS", "RITZ"]:
                raise ValueError("analysis_type must be 'EIGEN', 'LANCZOS', or 'RITZ'")
            
            # Validate type-specific required parameters
            if analysis_type in ["EIGEN"]:
                if ifreq is None:
                    raise ValueError("ifreq (Number of Frequencies) is required for EIGEN")
                if iiter is None:
                    raise ValueError("iiter (Number of Iterations) is required for EIGEN")
            
            # Handle LANCZOS parameters
            if analysis_type == "LANCZOS":
                # Handle new frequency_range format
                if frequency_range is not None:
                    if not isinstance(frequency_range, list) or len(frequency_range) != 2:
                        raise ValueError("frequency_range must be a list with exactly 2 elements [frmin, frmax]")
                    if frequency_range[0] >= frequency_range[1]:
                        raise ValueError("frmin must be less than frmax in frequency_range")
                    
                    # Automatically set parameters
                    bminmax = True
                    frmin = frequency_range[0]
                    frmax = frequency_range[1]
                else:
                    # Use legacy parameters or defaults
                    if bminmax is None:
                        bminmax = False
                    if bminmax and (frmin is None or frmax is None):
                        raise ValueError("frmin and frmax are required when bminmax is True for LANCZOS")
                    if frmin is not None and frmax is not None and frmin >= frmax:
                        raise ValueError("frmin must be less than frmax")
            
            # Handle RITZ parameters
            if analysis_type == "RITZ":
                if ignum is None:
                    raise ValueError("ignum (Number of Generations) is required for RITZ")
                
                # Handle new load_vector format
                if load_vector is not None:
                    if not isinstance(load_vector, list) or len(load_vector) == 0:
                        raise ValueError("load_vector must be a non-empty list")
                    
                    # Convert load_vector to vritz format
                    vritz = []
                    ground_acc_types = ["ACCX", "ACCY", "ACCZ"]
                    
                    for i, item in enumerate(load_vector):
                        if not isinstance(item, list) or len(item) != 2:
                            raise ValueError(f"load_vector[{i}] must be a list with exactly 2 elements [name, nog]")
                        
                        name, nog = item
                        if not isinstance(name, str):
                            raise ValueError(f"load_vector[{i}][0] (name) must be a string")
                        if not isinstance(nog, int) or nog <= 0:
                            raise ValueError(f"load_vector[{i}][1] (nog) must be a positive integer")
                        
                        # Determine if it's ground acceleration or case
                        if name in ground_acc_types:
                            vritz.append({
                                "KIND": "GROUND",
                                "GROUND": name,
                                "iNOG": nog
                            })
                        else:
                            vritz.append({
                                "KIND": "CASE",
                                "CASE": name,
                                "iNOG": nog
                            })
                
                # Use legacy vritz if provided and load_vector is not
                elif vritz is not None:
                    if not isinstance(vritz, list) or len(vritz) == 0:
                        raise ValueError("vritz (Load Cases) must be a non-empty list")
                    
                    # Validate legacy vritz format
                    for i, case in enumerate(vritz):
                        if not isinstance(case, dict):
                            raise ValueError(f"vritz[{i}] must be a dictionary")
                        if "KIND" not in case:
                            raise ValueError(f"vritz[{i}] must have 'KIND' key")
                        if case["KIND"] not in ["CASE", "GROUND"]:
                            raise ValueError(f"vritz[{i}]['KIND'] must be 'CASE' or 'GROUND'")
                        
                        if case["KIND"] == "GROUND":
                            if "GROUND" not in case or case["GROUND"] not in ["ACCX", "ACCY", "ACCZ"]:
                                raise ValueError(f"vritz[{i}] with KIND='GROUND' must have GROUND='ACCX'/'ACCY'/'ACCZ'")
                        elif case["KIND"] == "CASE":
                            if "CASE" not in case:
                                raise ValueError(f"vritz[{i}] with KIND='CASE' must have 'CASE' key")
                        
                        if "iNOG" not in case:
                            raise ValueError(f"vritz[{i}] must have 'iNOG' key")
                else:
                    raise ValueError("Either load_vector or vritz is required for RITZ analysis")
            
            # ID is always 1
            self.ID = 1
            
            # Set parameters
            self.TYPE = analysis_type
            self.iFREQ = ifreq
            self.iITER = iiter
            self.iDIM = idim
            self.TOL = tol
            self.bMINMAX = bminmax
            self.FRMIN = frmin
            self.FRMAX = frmax
            self.bSTRUM = bstrum
            self.bINCNL = bincnl
            self.iGNUM = ignum
            self.vRITZ = vritz
            
            # Add to static list
            AnalysisControl.EigenValue.data.append(self)
            
            # Automatically execute the data when instance is created
            self._execute()
        
        def _execute(self):
            """
            Automatically sends the Eigen Vector Analysis Control to the analysis system when created
            """
            json_data = {"Assign": {}}
            
            control_data = {"TYPE": self.TYPE}
            
            if self.TYPE in ["EIGEN", "LANCZOS"]:
                control_data.update({
                    "iFREQ": self.iFREQ,
                    "iITER": self.iITER,
                    "iDIM": self.iDIM,
                    "TOL": self.TOL
                })
                
                if self.TYPE == "LANCZOS":
                    control_data.update({
                        "bMINMAX": self.bMINMAX,
                        "FRMIN": self.FRMIN,
                        "FRMAX": self.FRMAX,
                        "bSTRUM": self.bSTRUM
                    })
            
            elif self.TYPE == "RITZ":
                control_data.update({
                    "bINCNL": self.bINCNL,
                    "iGNUM": self.iGNUM,
                    "vRITZ": self.vRITZ
                })
            
            json_data["Assign"][str(self.ID)] = control_data
            
            MidasAPI("PUT", "/db/eigv", json_data)

    class Settlement:
        
        data = []
        
        def __init__(self, 
                    concurrent_calc: bool = True,
                    concurrent_link: bool = True):
            """
            Settlement Analysis Control constructor for settlement analysis settings.
            
            Parameters:
                concurrent_calc: Plate Concurrent Force (default True, optional)
                    - Active: true
                    - Inactive: false
                
                concurrent_link: Elastic / General Links Concurrent Force (default True, optional)
                    - Active: true
                    - Inactive: false
            
            Examples:
                # with both Optional value
                Settlement()

                #without Optional value
                Settlement(
                    concurrent_calc=True,
                    concurrent_link=False
                )      

            """
            
            # ID is always 1
            self.ID = 1
            
            # Set parameters
            self.CONCURRENT_CALC = concurrent_calc
            self.CONCURRENT_LINK = concurrent_link
            
            # Add to static list
            AnalysisControl.Settlement.data.append(self)
            
            # Automatically execute the data when instance is created
            self._execute()
        
        def _execute(self):
            """
            Automatically sends the Settlement Analysis Control to the analysis system when created
            """
            json_data = {"Assign": {}}
            
            control_data = {
                "CONCURRENT_CALC": self.CONCURRENT_CALC,
                "CONCURRENT_LINK": self.CONCURRENT_LINK
            }
            
            json_data["Assign"][str(self.ID)] = control_data
            
            MidasAPI("PUT", "/db/smct", json_data)
