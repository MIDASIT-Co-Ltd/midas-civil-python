from ._mapi import *
from ._load import *


class BoundaryChangeAssignment:
    
    data = []
    
    def __init__(self,
                 # Support options
                 bSPT: bool = False,
                 bSPR: bool = False, 
                 bGSPR: bool = False,
                 bCGLINK: bool = False,
                 bSSSF: bool = False,
                 bPSSF: bool = False,
                 bRLS: bool = False,
                 bWSSF: bool = False,
                 bESSF: bool = False,
                 bCDOF: bool = False,
                 # Boundary settings
                 vBOUNDARY: list = None,
                 # Load analysis settings for ST type
                 ST_load_assignments: list = None,
                 # Load analysis settings for other types
                 MV: str = None,
                 SM: str = None,
                 THRSEV: str = None,
                 PO: str = None,
                 THNS: str = None,
                 ULAT: str = None):
        """
        Boundary Change Assignment constructor.
        
        Parameters:
            bSPT: Support (default False)
            bSPR: Point Spring Support (default False)
            bGSPR: General Spring Support (default False)
            bCGLINK: Change General Link Property (default False)
            bSSSF: Section Stiffness Scale Factor (default False)
            bPSSF: Plate Stiffness Scale Factor (default False)
            bRLS: Beam End Release (default False)
            bWSSF: Wall Stiffness Scale Factor (default False)
            bESSF: Element Stiffness Scale Factor (default False)
            bCDOF: Constrain DOF associated with specified displacements/Settlements by boundary group combinations (default False)
            vBOUNDARY: List of boundary assignments in format [["L1", "BG2"], ["L2", "BG1"]]
            ST_load_assignments: List of ST type load cases with BGCNAME assignments in format [["Self-weight", "L1"], ["SIDL", "UNCHANGED"]]
            MV, SM, THRSEV, PO, THNS, ULAT: Boundary group names for respective analysis types
            
        Examples:
            # Basic boundary change assignment
            BoundaryChangeAssignment(
                bSPT=True,
                bCDOF=True,
                vBOUNDARY=[["L1", "BG2"], ["L2", "BG1"]],
                ST_load_assignments=[["Self-weight", "L1"]],
                MV="L1"
            )
            
            # Complex assignment with multiple load types
            BoundaryChangeAssignment(
                bSPT=True,
                bSPR=False,
                bGSPR=False,
                vBOUNDARY=[["L1", "BG2"], ["L2", "BG1"]],
                ST_load_assignments=[["Self-weight", "L1"], ["SIDL", "L2"]],
                MV="L1",
                SM="L2",
                THRSEV="L1"
            )
        """
        
        # ID is always 1 based on the pattern
        self.ID = 1
        
        # Set support parameters
        self.bSPT = bSPT
        self.bSPR = bSPR
        self.bGSPR = bGSPR
        self.bCGLINK = bCGLINK
        self.bSSSF = bSSSF
        self.bPSSF = bPSSF
        self.bRLS = bRLS
        self.bWSSF = bWSSF
        self.bESSF = bESSF
        self.bCDOF = bCDOF
        
        # Process boundary data
        self.vBOUNDARY = self._process_boundary_data(vBOUNDARY)
        
        # Process load analysis data
        self.vLOADANAL = self._process_load_analysis_data(
            ST_load_assignments, MV, SM, THRSEV, PO, THNS, ULAT
        )
        
        # Add to static list
        BoundaryChangeAssignment.data.append(self)
        
        # Automatically execute the data when instance is created
        self._execute()
    
    def _process_boundary_data(self, vBOUNDARY):
        """
        Process boundary data from list format to required JSON structure.
        Input: [["L1", "BG2"], ["L2", "BG1"]]
        Output: [{"BGCNAME": "L1", "vBG": ["BG2"]}, {"BGCNAME": "L2", "vBG": ["BG1"]}]
        """
        if not vBOUNDARY:
            return []
        
        boundary_list = []
        for boundary_pair in vBOUNDARY:
            if len(boundary_pair) == 2:
                boundary_list.append({
                    "BGCNAME": boundary_pair[0],
                    "vBG": [boundary_pair[1]]
                })
        
        return boundary_list
    
    def _get_load_cases(self):
        """
        Get load cases from the system using Load_Case.get() command.
        This simulates the API call that would retrieve current load cases.
        """
        try:
            # This would be replaced with actual API call: Load_Case.get()
            # For now, using the provided example data structure
            load_cases_response = Load_Case.get()
            return load_cases_response.get('STLD', {})
        except:
            # Fallback to empty if API call fails
            return {}
    
    def _convert_st_assignments_to_dict(self, ST_load_assignments):
        """
        Convert ST_load_assignments from list format to dictionary format.
        Input: [["Self-weight", "L1"], ["SIDL", "UNCHANGED"]]
        Output: {"Self-weight": "L1", "SIDL": "UNCHANGED"}
        """
        if not ST_load_assignments:
            return {}
        
        assignments_dict = {}
        for assignment_pair in ST_load_assignments:
            if len(assignment_pair) == 2:
                assignments_dict[assignment_pair[0]] = assignment_pair[1]
        
        return assignments_dict
    
    def _process_load_analysis_data(self, ST_load_assignments, MV, SM, THRSEV, PO, THNS, ULAT):
        """
        Process load analysis data combining user input with system load cases.
        """
        load_anal_list = []
        
        # Get current load cases from system
        load_cases = self._get_load_cases()
        
        # Process ST type load cases
        st_cases = {case_data['NAME']: case_data for case_data in load_cases.values() }  # Assuming ST cases are USER type
        
        # Convert ST_load_assignments from list format to dictionary format for internal processing
        st_assignments_dict = self._convert_st_assignments_to_dict(ST_load_assignments)
        
        if st_cases:
            for case_name in st_cases.keys():
                bgcname = "UNCHANGED"  # Default value
                
                # If user provided specific assignment for this load case
                if st_assignments_dict and case_name in st_assignments_dict:
                    bgcname = st_assignments_dict[case_name]
                
                load_anal_list.append({
                    "TYPE": "ST",
                    "BGCNAME": bgcname,
                    "LCNAME": case_name
                })
        
        # Process other load analysis types
        analysis_types = {
            "MV": MV,
            "SM": SM,
            "THRSEV": THRSEV,
            "PO": PO,
            "THNS": THNS,
            "ULAT": ULAT
        }
        
        for analysis_type, bgcname in analysis_types.items():
            load_anal_entry = {
                "TYPE": analysis_type,
                "BGCNAME": bgcname if bgcname is not None else "UNCHANGED"
            }
            load_anal_list.append(load_anal_entry)
        
        return load_anal_list
    
    def _execute(self):
        """
        Automatically sends the BoundaryChangeAssignment to the system when created.
        """
        json_data = {"Assign": {}}
        
        boundary_data = {
            "bSPT": self.bSPT,
            "bSPR": self.bSPR,
            "bGSPR": self.bGSPR,
            "bCGLINK": self.bCGLINK,
            "bSSSF": self.bSSSF,
            "bPSSF": self.bPSSF,
            "bRLS": self.bRLS,
            "bWSSF": self.bWSSF,
            "bESSF": self.bESSF,
            "bCDOF": self.bCDOF,
            "vBOUNDARY": self.vBOUNDARY,
            "vLOADANAL": self.vLOADANAL
        }
        
        json_data["Assign"][str(self.ID)] = boundary_data
        
        # Execute the API call
        MidasAPI("PUT", "/db/bcct", json_data)
    
    def __str__(self):
        """
        String representation of the BoundaryChangeAssignment.
        """
        return f"BoundaryChangeAssignment(ID={self.ID}, Boundaries={len(self.vBOUNDARY)}, LoadAnalyses={len(self.vLOADANAL)})"
    
    def __repr__(self):
        """
        Detailed representation of the BoundaryChangeAssignment.
        """
        return (f"BoundaryChangeAssignment(ID={self.ID}, "
                f"bSPT={self.bSPT}, bCDOF={self.bCDOF}, "
                f"Boundaries={self.vBOUNDARY}, "
                f"LoadAnalyses={self.vLOADANAL})")



# Example usage:
"""
# Example 1: Basic boundary change assignment
boundary_assignment = BoundaryChangeAssignment(
    bSPT=True,
    bCDOF=True,
    vBOUNDARY=[["L1", "BG2"], ["L2", "BG1"]],
    ST_load_assignments=[["Self-weight", "L1"]],
    MV="L1"
)

# Example 2: Complex assignment with multiple settings
complex_assignment = BoundaryChangeAssignment(
    bSPT=True,
    bSPR=False,
    bGSPR=False,
    bCGLINK=False,
    bSSSF=False,
    bPSSF=False,
    bRLS=False,
    bCDOF=True,
    vBOUNDARY=[["L1", "BG2"], ["L2", "BG1"]],
    ST_load_assignments=[["Self-weight", "L1"], ["SIDL", "UNCHANGED"]],
    MV="UNCHANGED",
    SM="L2",
    THRSEV="L1",
    PO="UNCHANGED",
    THNS="UNCHANGED",
    ULAT="UNCHANGED"
)

# Example 3: Minimal assignment with defaults
minimal_assignment = BoundaryChangeAssignment(
    bSPT=True,
    vBOUNDARY=[["L1", "BG2"]]
)
"""