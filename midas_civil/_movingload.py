
from ._mapi import *
from ._model import *

# ----------------------------------------------------------------------------------------------------------------

def _El_list(Start_id: int, End_id: int) -> list:

    return list(range(Start_id, End_id + 1))

# --------------------------------------------------------------------------------------------------------------------------

class MovingLoad:


    @classmethod
    def create(cls):
            
            if cls.LineLane.lanes:
                cls.LineLane.create()
            
            if cls.Vehicle.vehicles:
                cls.Vehicle.create()
                
            if cls.Case.cases:
                cls.Case.create()

    @classmethod
    def delete(cls):
            cls.Code.delete()

    @classmethod
    def sync(cls):
    
            cls.LineLane.sync()
            cls.Vehicle.sync()
            cls.Case.sync()

    
    class Code:
   
        
        def __init__(self, code_name: str):
            """
            code_name (str): The name of the moving load code to be used.
            
            Available Moving Load Codes:
            - "KSCE-LSD15", "KOREA", "AASHTO STANDARD", "AASHTO LRFD", 
            - "AASHTO LRFD(PENNDOT)", "CHINA", "INDIA", "TAIWAN", "CANADA", 
            - "BS", "EUROCODE", "AUSTRALIA", "POLAND", "RUSSIA", 
            - "SOUTH AFRICA"
            """
            valid_codes = {
                "KSCE-LSD15", "KOREA", "AASHTO STANDARD", "AASHTO LRFD", "AASHTO LRFD(PENDOT)", 
                "CHINA", "INDIA", "TAIWAN", "CANADA", "BS", "EUROCODE", "AUSTRALIA", 
                "POLAND", "RUSSIA", "SOUTH AFRICA"
            }

            if code_name not in valid_codes:
                raise ValueError(f"Invalid code_name. Choose from: {', '.join(valid_codes)}")

            self.code_name = code_name
            json_data = {
                "Assign": {
                    "1": {
                        "CODE": code_name
                    }
                }
            }
            MidasAPI("PUT", "/db/mvcd", json_data)

        @classmethod
        def get(cls):
            """Gets the currently set moving load code from the Midas model."""
            return MidasAPI("GET", "/db/mvcd")
        
        @classmethod
        def delete(cls):
            return MidasAPI("DELETE", "/db/mvcd")

#------------------------------------------------------------------------------------------------------------------------------------- 
    class LineLane:
    
        lanes = []
        
        def __init__(
            self,
            code: str,
            Lane_name: str,
            Ecc: float,
            Wheel_space: float,
            Elment_start: int,
            Elemnt_end: int,
            IF: float = 0,
            Span: float = 0,
            id: int = None,
            width: float = 0,
            opt_width: float = 0,
            Group_Name: str = "",
            Moving_Direction: str = "BOTH",
            Skew_start: float = 0,
            Skew_end: float = 0
        ):
            """
                code (str): Country code for traffic lane standards (e.g., "INDIA", "CHINA").
                Lane_name (str): A unique name for the lane.
                Ecc (float): Lateral eccentricity of the lane's centerline from the reference element path.
                               A positive value indicates an offset in the +Y direction of the element's local axis.
                Wheel_space (float): The center-to-center distance between the wheels of the vehicle.
                                     (e.g., a standard value is often around 1.8m or 6ft).
                Elment_start (int): The first element ID in the continuous path defining the lane.
                Elemnt_end (int): The last element ID in the continuous path defining the lane.
                IF (float, optional): Impact Factor or Scale Factor, as defined by the selected design code. Defaults to 0.(For LRFD code Add Centerifugal force Input)
                Span (float, optional): The span length of the lane, used by some codes for impact factor calculation. Defaults to 0.
                id (int, optional): A unique integer ID for the lane. If None, it will be auto-assigned. Defaults to None.
                width (float, optional): The width of the traffic lane. Key name "WIDTH". Defaults to 0.
                opt_width (float, optional): The allowable width of the traffic lane for auto-positioning. Key name "ALLOW_WIDTH". Defaults to 0.
                Group_Name (str, optional): The group name for cross-beam load distribution. If provided, distribution is "CROSS". Defaults to "".
                Moving_Direction (str, optional): The allowed direction of vehicle movement ("FORWARD", "BACKWARD", "BOTH"). Defaults to "BOTH".
                Skew_start (float, optional): The skew angle of the bridge at the start of the lane (in degrees). Defaults to 0.
                Skew_end (float, optional): The skew angle of the bridge at the end of the lane (in degrees). Defaults to 0.
            """
            self.code = code
            self.Lane_name = Lane_name
            self.Ecc = Ecc
            self.Wheel_space = Wheel_space
            self.Elment_start = Elment_start
            self.Elemnt_end = Elemnt_end
            self.IF = IF
            self.Span = Span
            self.id = len(MovingLoad.LineLane.lanes) + 1 if id is None else id
            self.width = width
            self.opt_width = opt_width
            self.Group_Name = Group_Name
            self.Moving_Direction = Moving_Direction
            self.Skew_start = Skew_start
            self.Skew_end = Skew_end
            
            # Ensure the correct moving load code is active in the model
            MovingLoad.Code(code)
            
            # Avoid duplicating lanes if syncing
            if not any(lane.id == self.id for lane in MovingLoad.LineLane.lanes):
                MovingLoad.LineLane.lanes.append(self)

        # Definition of country-specific subclasses
        class India:
            def __init__(self, Lane_name: str, Ecc: float, Wheel_space: float, Elment_start: int, 
                        Elemnt_end: int, IF: float = 0, Span: float = 0, id: int = None,
                        width: float = 0, opt_width: float = 0, Group_Name: str = "", Moving_Direction: str = "BOTH",
                        Skew_start: float = 0, Skew_end: float = 0):
                """Defines a traffic lane according to Indian standards."""
                MovingLoad.LineLane("INDIA", Lane_name, Ecc, Wheel_space, Elment_start, Elemnt_end,
                                    IF, Span, id, width, opt_width, Group_Name, Moving_Direction, Skew_start, Skew_end)

        class China:
            def __init__(self, Lane_name: str, Ecc: float, Wheel_space: float, Elment_start: int, 
                        Elemnt_end: int, IF: float = 0, Span: float = 0, id: int = None,
                        width: float = 0, opt_width: float = 0, Group_Name: str = "", Moving_Direction: str = "BOTH",
                        Skew_start: float = 0, Skew_end: float = 0):
                """Defines a traffic lane according to Chinese standards."""
                MovingLoad.LineLane("CHINA", Lane_name, Ecc, Wheel_space, Elment_start, Elemnt_end,
                                    IF, Span, id, width, opt_width, Group_Name, Moving_Direction, Skew_start, Skew_end)

        class Korea:
            def __init__(self, Lane_name: str, Ecc: float, Wheel_space: float, Elment_start: int, 
                        Elemnt_end: int, IF: float = 0, id: int = None, opt_width: float = 0,
                        Group_Name: str = "", Moving_Direction: str = "BOTH",
                        Skew_start: float = 0, Skew_end: float = 0):
                """Defines a traffic lane according to Korean standards."""
                MovingLoad.LineLane("KOREA", Lane_name, Ecc, Wheel_space, Elment_start, Elemnt_end,
                                    IF, 0, id, 3, opt_width, Group_Name, Moving_Direction, Skew_start, Skew_end)
        
        class Taiwan:
            def __init__(self, Lane_name: str, Ecc: float, Wheel_space: float, Elment_start: int, 
                        Elemnt_end: int, IF: float = 0, id: int = None, width: float = 0, opt_width: float = 0,
                        Group_Name: str = "", Moving_Direction: str = "BOTH",
                        Skew_start: float = 0, Skew_end: float = 0):
                """Defines a traffic lane according to Taiwanese standards."""
                MovingLoad.LineLane("TAIWAN", Lane_name, Ecc, Wheel_space, Elment_start, Elemnt_end,
                                    IF, 0, id, width, opt_width, Group_Name, Moving_Direction, Skew_start, Skew_end)

        class AASHTOStandard:
            def __init__(self, Lane_name: str, Ecc: float, Wheel_space: float, Elment_start: int, 
                        Elemnt_end: int, IF: float = 0, id: int = None, opt_width: float = 0,
                        Group_Name: str = "", Moving_Direction: str = "BOTH",
                        Skew_start: float = 0, Skew_end: float = 0):
                """Defines a traffic lane according to AASHTO Standard."""
                MovingLoad.LineLane("AASHTO STANDARD", Lane_name, Ecc, Wheel_space, Elment_start, Elemnt_end,
                                    IF, 0, id, 3, opt_width, Group_Name, Moving_Direction, Skew_start, Skew_end)

        class AASHTOLRFD:
            def __init__(self, Lane_name: str, Ecc: float, Wheel_space: float, Elment_start: int, 
                        Elemnt_end: int, IF: float = 0, id: int = None, opt_width: float = 0,
                        Group_Name: str = "", Moving_Direction: str = "BOTH",
                        Skew_start: float = 0, Skew_end: float = 0):
                """Defines a traffic lane according to AASHTO LRFD."""
                MovingLoad.LineLane("AASHTO LRFD", Lane_name, Ecc, Wheel_space, Elment_start, Elemnt_end,
                                    IF, 0, id, 3, opt_width, Group_Name, Moving_Direction, Skew_start, Skew_end)

        class PENNDOT:
            def __init__(self, Lane_name: str, Ecc: float, Wheel_space: float, Elment_start: int, 
                        Elemnt_end: int, id: int = None, opt_width: float = 0,
                        Group_Name: str = "", Moving_Direction: str = "BOTH",
                        Skew_start: float = 0, Skew_end: float = 0):
                """Defines a traffic lane according to AASHTO LRFD (PENNDOT)."""
                MovingLoad.LineLane("AASHTO LRFD(PENDOT)", Lane_name, Ecc, Wheel_space, Elment_start, Elemnt_end,
                                    0, 0, id, 3, opt_width, Group_Name, Moving_Direction, Skew_start, Skew_end)

        class Canada:
            def __init__(self, Lane_name: str, Ecc: float, Wheel_space: float, Elment_start: int, 
                        Elemnt_end: int, id: int = None, opt_width: float = 0,
                        Group_Name: str = "", Moving_Direction: str = "BOTH",
                        Skew_start: float = 0, Skew_end: float = 0):
                """Defines a traffic lane according to Canadian standards."""
                MovingLoad.LineLane("CANADA", Lane_name, Ecc, Wheel_space, Elment_start, Elemnt_end,
                                    0, 0, id, 3, opt_width, Group_Name, Moving_Direction, Skew_start, Skew_end)

        class BS:
            def __init__(self, Lane_name: str, Ecc: float, Wheel_space: float, Elment_start: int, 
                        Elemnt_end: int, id: int = None, width: float = 0, opt_width: float = 0,
                        Group_Name: str = "", Moving_Direction: str = "BOTH",
                        Skew_start: float = 0, Skew_end: float = 0):
                """Defines a traffic lane according to British Standards (BS)."""
                MovingLoad.LineLane("BS", Lane_name, Ecc, Wheel_space, Elment_start, Elemnt_end,
                                    0, 0, id, width, opt_width, Group_Name, Moving_Direction, Skew_start, Skew_end)

        class Eurocode:
            def __init__(self, Lane_name: str, Ecc: float, Wheel_space: float, Elment_start: int, 
                        Elemnt_end: int, IF: float = 0, id: int = None, width: float = 0, opt_width: float = 0,
                        Group_Name: str = "", Moving_Direction: str = "BOTH",
                        Skew_start: float = 0, Skew_end: float = 0):
                """Defines a traffic lane according to Eurocode."""
                MovingLoad.LineLane("EUROCODE", Lane_name, Ecc, Wheel_space, Elment_start, Elemnt_end,
                                    IF, 0, id, width, opt_width, Group_Name, Moving_Direction, Skew_start, Skew_end)

        class Australia:
            def __init__(self, Lane_name: str, Ecc: float, Wheel_space: float, Elment_start: int, 
                        Elemnt_end: int, id: int = None, width: float = 0, opt_width: float = 0,
                        Group_Name: str = "", Moving_Direction: str = "BOTH",
                        Skew_start: float = 0, Skew_end: float = 0):
                """Defines a traffic lane according to Australian standards."""
                MovingLoad.LineLane("AUSTRALIA", Lane_name, Ecc, Wheel_space, Elment_start, Elemnt_end,
                                    0, 0, id, width, opt_width, Group_Name, Moving_Direction, Skew_start, Skew_end)

        class Poland:
            def __init__(self, Lane_name: str, Ecc: float, Wheel_space: float, Elment_start: int, 
                        Elemnt_end: int, id: int = None, width: float = 0, opt_width: float = 0,
                        Group_Name: str = "", Moving_Direction: str = "BOTH",
                        Skew_start: float = 0, Skew_end: float = 0):
                """Defines a traffic lane according to Polish standards."""
                MovingLoad.LineLane("POLAND", Lane_name, Ecc, Wheel_space, Elment_start, Elemnt_end,
                                    0, 0, id, width, opt_width, Group_Name, Moving_Direction, Skew_start, Skew_end)

        class Russia:
            def __init__(self, Lane_name: str, Ecc: float, Wheel_space: float, Elment_start: int, 
                        Elemnt_end: int, id: int = None, width: float = 0, opt_width: float = 0,
                        Group_Name: str = "", Moving_Direction: str = "BOTH",
                        Skew_start: float = 0, Skew_end: float = 0):
                """Defines a traffic lane according to Russian standards."""
                MovingLoad.LineLane("RUSSIA", Lane_name, Ecc, Wheel_space, Elment_start, Elemnt_end,
                                    0, 0, id, width, opt_width, Group_Name, Moving_Direction, Skew_start, Skew_end)

        class SouthAfrica:
            def __init__(self, Lane_name: str, Ecc: float, Wheel_space: float, Elment_start: int, 
                        Elemnt_end: int, id: int = None, width: float = 0, opt_width: float = 0,
                        Group_Name: str = "", Moving_Direction: str = "BOTH",
                        Skew_start: float = 0, Skew_end: float = 0):
                """Defines a traffic lane according to South African standards."""
                MovingLoad.LineLane("SOUTH AFRICA", Lane_name, Ecc, Wheel_space, Elment_start, Elemnt_end,
                                    0, 0, id, width, opt_width, Group_Name, Moving_Direction, Skew_start, Skew_end)

        class KSCELSD15:
            def __init__(self, Lane_name: str, Ecc: float, Wheel_space: float, Elment_start: int, 
                        Elemnt_end: int, id: int = None, opt_width: float = 0,
                        Group_Name: str = "", Moving_Direction: str = "BOTH",
                        Skew_start: float = 0, Skew_end: float = 0):
                """Defines a traffic lane according to KSCE-LSD15."""
                MovingLoad.LineLane("KSCE-LSD15", Lane_name, Ecc, Wheel_space, Elment_start, Elemnt_end,
                                    0, 0, id, 3, opt_width, Group_Name, Moving_Direction, Skew_start, Skew_end)

        @staticmethod
        def _get_lane_item_details(code, lane, is_start_span):
            """
            Internal helper to get code-specific keys for a LANE_ITEM.
            This centralizes the logic for different country standards.
            """
            details = {}
            if code == "INDIA":
                details = {
                    "SPAN": lane.Span,
                    "IMPACT_SPAN": 1 if lane.Span > 0 else 0,
                    "IMPACT_FACTOR": lane.IF
                }
            elif code == "CHINA":
                details = {
                    "SPAN": lane.Span,
                    "SPAN_START": is_start_span,
                    "SCALE_FACTOR": lane.IF
                }
            elif code in ["KOREA", "TAIWAN", "AASHTO STANDARD"]:
                details = {
                    "FACT": lane.IF,
                    "SPAN_START": is_start_span
                }
            elif code in ["AASHTO LRFD(PENDOT)", "AUSTRALIA", "POLAND"]:
                details = {
                    "SPAN_START": is_start_span
                }
            elif code == "AASHTO LRFD":
                details = {
                    "CENT_F": lane.IF,
                    "SPAN_START": is_start_span
                }
            elif code == "EUROCODE":
                details = {
                    "ECCEN_VERT_LOAD": lane.IF
                }
            # Codes like "KSCE-LSD15", "BS", "CANADA" etc., don't need extra keys
            
            return details

        @classmethod
        def json(cls, lanes_list=None):
            """
            Generates the JSON 
            """
            if lanes_list is None:
                lanes_list = cls.lanes

            data = {"Assign": {}}
            for lane in lanes_list:
                E_list = _El_list(lane.Elment_start, lane.Elemnt_end)
                Load_Dist = "CROSS" if lane.Group_Name else "LANE"
                opt_auto_lane = lane.width > 0 or lane.opt_width > 0

                common_data = {
                    "LL_NAME": lane.Lane_name,
                    "LOAD_DIST": Load_Dist,
                    "GROUP_NAME": lane.Group_Name if Load_Dist == "CROSS" else "",
                    "SKEW_START": lane.Skew_start,
                    "SKEW_END": lane.Skew_end,
                    "MOVING": lane.Moving_Direction,
                    "WHEEL_SPACE": lane.Wheel_space,
                    "WIDTH": lane.width,
                    "OPT_AUTO_LANE": opt_auto_lane,
                    "ALLOW_WIDTH": lane.opt_width
                }

                lane_items = []
                for i, e in enumerate(E_list):
                    is_start_span = (i == 0)
                    # Get code-specific details from the helper function
                    item_details = cls._get_lane_item_details(lane.code, lane, is_start_span)
                    
                    # Start with the base item
                    lane_item = {"ELEM": e, "ECC": lane.Ecc}
                    # Add the code-specific details
                    lane_item.update(item_details)
                    lane_items.append(lane_item)

                data["Assign"][str(lane.id)] = {
                    "COMMON": common_data,
                    "LANE_ITEMS": lane_items
                }
            return data
        
        @classmethod
        def create(cls):
            """Sends all defined traffic lane data to the Midas Civil API """
            if not cls.lanes:
                print("No lanes to create.")
                return
            
            # Group lanes by their country code to use the correct API endpoint
            lanes_by_code = {"INDIA": [], "CHINA": [], "OTHER": []}
            for lane in cls.lanes:
                if lane.code == "INDIA":
                    lanes_by_code["INDIA"].append(lane)
                elif lane.code == "CHINA":
                    lanes_by_code["CHINA"].append(lane)
                else:
                    lanes_by_code["OTHER"].append(lane)
            
            # Create JSON and send data for each group
            if lanes_by_code["INDIA"]:
                india_data = cls.json(lanes_by_code["INDIA"])
                MidasAPI("PUT", "/db/llanid", india_data)
            
            if lanes_by_code["CHINA"]:
                china_data = cls.json(lanes_by_code["CHINA"])
                MidasAPI("PUT", "/db/llanch", china_data)
            
            if lanes_by_code["OTHER"]:
                other_data = cls.json(lanes_by_code["OTHER"])
                MidasAPI("PUT", "/db/llan", other_data)

        @classmethod
        def get(cls):
            """Retrieves all lane data from the Midas model"""
            all_lanes_data = {"LANE_DATA": {}}
            
            endpoints = {
                "/db/llanid": ("INDIA", "LLANID"),
                "/db/llanch": ("CHINA", "LLANCH"),
                "/db/llan": ("OTHER", "LLAN")
            }

            for endpoint, (code_type, response_key) in endpoints.items():
                api_data = MidasAPI("GET", endpoint)
                if api_data and response_key in api_data:
                    for lane_id, lane_details in api_data[response_key].items():
                        if 'COMMON' in lane_details:
                            lane_details['COMMON']['CODE_TYPE'] = code_type
                        all_lanes_data["LANE_DATA"][lane_id] = lane_details
            
            return all_lanes_data


        @classmethod
        def delete(cls):
            """Deletes all traffic lanes from the Midas model."""
            all_lanes_in_model = cls.get().get("LANE_DATA", {})
            if not all_lanes_in_model:
                print("No lanes found in the model. Nothing to delete.")
                return

            target_ids = [int(id_str) for id_str in all_lanes_in_model.keys()]
            
            if not target_ids:
                print("No target lanes to delete.")
                return

            ids_to_delete = {"INDIA": [], "CHINA": [], "OTHER": []}
            for lane_id in target_ids:
                lane_id_str = str(lane_id)
                code_type = all_lanes_in_model[lane_id_str].get("COMMON", {}).get("CODE_TYPE", "OTHER")
                ids_to_delete[code_type].append(lane_id)

            if ids_to_delete["INDIA"]:
                MidasAPI("DELETE", "/db/llanid", {"Remove": ids_to_delete["INDIA"]})
            if ids_to_delete["CHINA"]:
                MidasAPI("DELETE", "/db/llanch", {"Remove": ids_to_delete["CHINA"]})
            if ids_to_delete["OTHER"]:
                MidasAPI("DELETE", "/db/llan", {"Remove": ids_to_delete["OTHER"]})
            
        @classmethod
        def sync(cls):
            """
            Synchronizes the lane data from the Midas model 
            """
            # Clear existing lanes
            cls.lanes = []
            
            # Get the current active code from the model
            try:
                code_response = MovingLoad.Code.get()
                if not code_response or 'MVCD' not in code_response:
                    print("Warning: No moving load code found in model. Cannot sync lanes.")
                    return
                
                # Extract the active code name
                current_code = None
                mvcd_data = code_response.get('MVCD', {})
                for code_id, code_info in mvcd_data.items():
                    if isinstance(code_info, dict) and 'CODE' in code_info:
                        current_code = code_info['CODE']
                        break
                
                if not current_code:
                    print("Warning: Could not determine active moving load code. Cannot sync lanes.")
                    return
                    
            except Exception as e:
                print(f"Error getting current code: {e}")
                return
            
            # Get all lane data from the model
            response = cls.get()
            all_lanes_data = response.get("LANE_DATA", {})
            
            if not all_lanes_data:
                print("No lane data found in model to sync.")
                return

            # Process each lane from the model
            for lane_id, lane_data in all_lanes_data.items():
                common = lane_data.get("COMMON", {})
                items = lane_data.get("LANE_ITEMS", [])
                
                if not common or not items:
                    continue

                # Extract element list to find start and end
                element_ids = [item['ELEM'] for item in items]
                if not element_ids:
                    continue
                el_start = min(element_ids)
                el_end = max(element_ids)
                
                # Extract common properties
                lane_name = common.get("LL_NAME", f"Lane_{lane_id}")
                ecc = items[0].get("ECC", 0) if items else 0
                wheel_space = common.get("WHEEL_SPACE", 0)
                width = common.get("WIDTH", 0)
                opt_width = common.get("ALLOW_WIDTH", 0)
                group_name = common.get("GROUP_NAME", "")
                moving_dir = common.get("MOVING", "BOTH")
                skew_start = common.get("SKEW_START", 0)
                skew_end = common.get("SKEW_END", 0)
                
                # Extract code-specific parameters based on the current active code
                if_val = 0
                span_val = 0
                
                # Use the first item to extract code-specific parameters
                first_item = items[0] if items else {}
                
                if current_code == "INDIA":
                    if_val = first_item.get("IMPACT_FACTOR", 0)
                    span_val = first_item.get("SPAN", 0)
                elif current_code == "CHINA":
                    if_val = first_item.get("SCALE_FACTOR", 0)
                    span_val = first_item.get("SPAN", 0)
                elif current_code in ["KOREA", "TAIWAN", "AASHTO STANDARD"]:
                    if_val = first_item.get("FACT", 0)
                elif current_code == "AASHTO LRFD":
                    if_val = first_item.get("CENT_F", 0)
                elif current_code == "EUROCODE":
                    if_val = first_item.get("ECCEN_VERT_LOAD", 0)
                # For codes like "KSCE-LSD15", "AASHTO LRFD(PENDOT)", "BS", "CANADA", 
                # "AUSTRALIA", "POLAND", "RUSSIA", "SOUTH AFRICA" - they don't have specific IF parameters
                
                # Create the LineLane object with the current active code
                try:
                    lane_obj = MovingLoad.LineLane(
                        code=current_code,
                        Lane_name=lane_name,
                        Ecc=ecc,
                        Wheel_space=wheel_space,
                        Elment_start=el_start,
                        Elemnt_end=el_end,
                        IF=if_val,
                        Span=span_val,
                        id=int(lane_id),
                        width=width,
                        opt_width=opt_width,
                        Group_Name=group_name,
                        Moving_Direction=moving_dir,
                        Skew_start=skew_start,
                        Skew_end=skew_end
                    )
                    # print(f"Synced lane '{lane_name}' (ID: {lane_id}) with code '{current_code}'")
                    
                except Exception as e:
                    print(f"Error creating lane {lane_id}: {e}")
                    continue
 # =============================================  VEHICLE CLASS  =================================================================
    

    class Vehicle:

        vehicles = []

        # --- Data mapping for Indian (IRS) vehicle codes ---
        _irs_vehicle_map = {
            "BG-1676": {
                "full_name": "Broad Gauge-1676mm",
                "vehicles": [
                    "Modified B.G. Loading 1987-1", "Modified B.G. Loading 1987-2", "B.G. Standard Loading 1926-M.L.",
                    "B.G. Standard Loading 1926-B.L.", "Revised B.G. Loading 1975-WG1+WG1", "Revised B.G. Loading 1975-WAM4A+WAM4A",
                    "Revised B.G. Loading 1975-Bo-Bo+Bo-Bo", "Revised B.G. Loading 1975-WAM4A", "Revised B.G. Loading 1975-WAM4A+WAM4",
                    "Revised B.G. Loading 1975-WAM4A+WDM2", "25t Loading-2008 Combination 1", "25t Loading-2008 Combination 2",
                    "25t Loading-2008 Combination 3", "25t Loading-2008 Combination 4", "25t Loading-2008 Combination 5",
                    "DFC Loading Combination 1", "DFC Loading Combination 2", "DFC Loading Combination 3",
                    "DFC Loading Combination 4", "DFC Loading Combination 5"
                ]
            },
            "MG-1000": {
                "full_name": "Metre Gauge-1000mm",
                "vehicles": ["2 Co-Co Locomotives", "2 Bo-Bo Locomotives", "MGML Loading of 1929", "M.L.", "B.L.", "C."]
            },
            "NG-762": {
                "full_name": "Narrow Gauge-762mm",
                "vehicles": [
                    "Class H: B-B or Bo-Bo Type", "Class H: C-C or Co-Co Type", "Class H: Steam (Zf/1)", "Class H: Diesel Electric",
                    "Class A: B-B or Bo-Bo Type", "Class A: C-C or Co-Co Type", "Class A: Diesel Mech./Elec.",
                    "Class A: Diesel Mech./Elec.(Articulated)", "Class A: DRG No. CSO/C-873", "Class B: B-B or Bo-Bo Type",
                    "Class B: Steam Engine (Tank)", "Class B: Steam Engine (Tender)", "Class B: Diesel Electric"
                ]
            },
            "HML": {
                "full_name": "Heavy Mineral Loadings",
                "vehicles": [f"Train Formation No.{i}" for i in range(1, 18)]
            },
            "FTB": {
                "full_name": "Footbridge & Footpath",
                "vehicles": ["Footbridge & Footpath"]
            }
        }
        
        # --- Default parameter mapping for Indian vehicle codes ---
        _india_defaults_map = {
            "IRC": {
                "Footway": {"VEH_IN": {"FOOTWAY": 4.903325, "FOOTWAY_WIDTH": 3}}
            },
            "IRS": {
                "BG-1676": {
                    "Modified B.G. Loading 1987-1": {"VEH_IN": {"TRACTIVE": 490.3325, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "Modified B.G. Loading 1987-2": {"VEH_IN": {"TRACTIVE": 490.3325, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "B.G. Standard Loading 1926-M.L.": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "B.G. Standard Loading 1926-B.L.": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "Revised B.G. Loading 1975-WG1+WG1": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "Revised B.G. Loading 1975-WAM4A+WAM4A": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "Revised B.G. Loading 1975-Bo-Bo+Bo-Bo": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "Revised B.G. Loading 1975-WAM4A": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "Revised B.G. Loading 1975-WAM4A+WAM4": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "Revised B.G. Loading 1975-WAM4A+WDM2": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "25t Loading-2008 Combination 1": {"VEH_IN": {"TRACTIVE": 617.81895, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "25t Loading-2008 Combination 2": {"VEH_IN": {"TRACTIVE": 509.9458, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "25t Loading-2008 Combination 3": {"VEH_IN": {"TRACTIVE": 823.7586, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "25t Loading-2008 Combination 4": {"VEH_IN": {"TRACTIVE": 490.3325, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "25t Loading-2008 Combination 5": {"VEH_IN": {"TRACTIVE": 490.3325, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "DFC Loading Combination 1": {"VEH_IN": {"TRACTIVE": 617.81895, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "DFC Loading Combination 2": {"VEH_IN": {"TRACTIVE": 509.9458, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "DFC Loading Combination 3": {"VEH_IN": {"TRACTIVE": 823.7586, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "DFC Loading Combination 4": {"VEH_IN": {"TRACTIVE": 490.3325, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "DFC Loading Combination 5": {"VEH_IN": {"TRACTIVE": 490.3325, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                },
                "MG-1000": {
                    "2 Co-Co Locomotives": {"VEH_IN": {"TRACTIVE": 313.8128, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "2 Bo-Bo Locomotives": {"VEH_IN": {"TRACTIVE": 235.3596, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "MGML Loading of 1929": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "M.L.": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "B.L.": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "C.": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                },
                "NG-762": {
                    "Class H: B-B or Bo-Bo Type": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "Class H: C-C or Co-Co Type": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "Class H: Steam (Zf/1)": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "Class H: Diesel Electric": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "Class A: B-B or Bo-Bo Type": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "Class A: C-C or Co-Co Type": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "Class A: Diesel Mech./Elec.": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "Class A: Diesel Mech./Elec.(Articulated)": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "Class A: DRG No. CSO/C-873": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "Class B: B-B or Bo-Bo Type": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "Class B: Steam Engine (Tank)": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "Class B: Steam Engine (Tender)": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                    "Class B: Diesel Electric": {"VEH_IN": {"TRACTIVE": 0, "BRAKE_LOCO_RATIO": 25, "BRAKE_TRAIN_RATIO": 13.4}},
                },
                "HML": {
                    "Train Formation No.1": {"VEH_IN": {"TRACTIVE": 588.399, "BRAKE_LOCO": 245.16625}},
                    "Train Formation No.2": {"VEH_IN": {"TRACTIVE": 588.399, "BRAKE_LOCO": 245.16625}},
                    "Train Formation No.3": {"VEH_IN": {"TRACTIVE": 588.399, "BRAKE_LOCO": 245.16625}},
                    "Train Formation No.4": {"VEH_IN": {"TRACTIVE": 588.399, "BRAKE_LOCO": 245.16625}},
                    "Train Formation No.5": {"VEH_IN": {"TRACTIVE": 441.29925, "BRAKE_LOCO": 245.16625}},
                    "Train Formation No.6": {"VEH_IN": {"TRACTIVE": 441.29925, "BRAKE_LOCO": 245.16625}},
                    "Train Formation No.7": {"VEH_IN": {"TRACTIVE": 441.29925, "BRAKE_LOCO": 245.16625}},
                    "Train Formation No.8": {"VEH_IN": {"TRACTIVE": 298.61249, "BRAKE_LOCO": 215.7463}},
                    "Train Formation No.9": {"VEH_IN": {"TRACTIVE": 397.169325, "BRAKE_LOCO": 114.737805}},
                    "Train Formation No.10": {"VEH_IN": {"TRACTIVE": 397.169325, "BRAKE_LOCO": 114.737805}},
                    "Train Formation No.11": {"VEH_IN": {"TRACTIVE": 397.169325, "BRAKE_LOCO": 114.737805}},
                    "Train Formation No.12": {"VEH_IN": {"TRACTIVE": 441.29925, "BRAKE_LOCO": 245.16625}},
                    "Train Formation No.13": {"VEH_IN": {"TRACTIVE": 441.29925, "BRAKE_LOCO": 245.16625}},
                    "Train Formation No.14": {"VEH_IN": {"TRACTIVE": 441.29925, "BRAKE_LOCO": 245.16625}},
                    "Train Formation No.15": {"VEH_IN": {"TRACTIVE": 441.29925, "BRAKE_LOCO": 245.16625}},
                    "Train Formation No.16": {"VEH_IN": {"TRACTIVE": 441.29925, "BRAKE_LOCO": 245.16625}},
                    "Train Formation No.17": {"VEH_IN": {"TRACTIVE": 441.29925, "BRAKE_LOCO": 245.16625}},
                },
                "FTB": {
                    "Footbridge & Footpath": {"VEH_IN": {"FOOTWAY_WIDTH": 3, "SPAN_LENGTH": 7.5}}
                }
            }
        }
        
        # --- Data mapping for Eurocode vehicle codes ---
        _euro_vehicle_map = {
            "RoadBridge": {
                "full_name": "EN 1991-2:2003 - Road Bridge", "sub_type": 19,
                "vehicle_types": [
                    {"name": "Load Model 1", "defaults": {"AMP_VALUES": [0.75, 0.4], "TANDEM_ADJUST_VALUES": [1,1,1], "UDL_ADJUST_VALUES": [1,1,1,1]}},
                    {"name": "Load Model 2", "defaults": {"ADJUSTMENT": 0.75, "ADJUSTMENT2": 1}},
                    {"name": "Load Model 4", "defaults": {"ADJUSTMENT": 0.75}},
                    {"name": "Load Model 3", "selectable_vehicles": ["600/150", "900/150", "1200/150/200", "1500/150/200", "1800/150/200", "2400/200", "3000/200", "3600/200"], "defaults": {"LM3_LOADCASE1": True, "LM3_LOADCASE2": False, "DYNAMIC_FACTOR": True, "USER_INPUT": False}},
                    {"name": "Load Model 3 (UK NA)", "selectable_vehicles": ["SV 80", "SV 100", "SV 196", "SOV 250", "SOV 350", "SOV 450", "SOV 600"], "defaults": {"DYNAMIC_FACTOR": True, "USER_INPUT": False}}
                ]
            },
            "FTB": {
                "full_name": "EN 1991-2:2003 - Footway and FootBridge", "sub_type": 20,
                "vehicle_types": [
                    {"name": "Uniform load (Road bridge footway)", "defaults": {"ADJUSTMENT": 0.4, "FOOTWAY": 5}},
                    {"name": "Uniform load (Footbridge)", "defaults": {"ADJUSTMENT": 0.4}},
                    {"name": "Concentrated Load", "defaults": {}},
                    {"name": "Uniform load (Road bridge footway) UK NA", "defaults": {"ADJUSTMENT": 0.4}}
                ]
            },
            "RoadBridgeFatigue": {
                "full_name": "EN 1991-2:2003 - RoadBridge Fatigue", "sub_type": 21,
                "vehicle_types": [
                    {"name": "Fatigue Load Model 1", "defaults": {"AMP": 1, "TANDEM_ADJUST_VALUES": [1,1,1], "UDL_ADJUST_VALUES": [1,1,1,1]}},
                    {"name": "Fatigue Load Model 2 (280)", "defaults": {"AMP": 1}},
                    {"name": "Fatigue Load Model 2 (360)", "defaults": {"AMP": 1}},
                    {"name": "Fatigue Load Model 2 (630)", "defaults": {"AMP": 1}},
                    {"name": "Fatigue Load Model 2 (560)", "defaults": {"AMP": 1}},
                    {"name": "Fatigue Load Model 2 (610)", "defaults": {"AMP": 1}},
                    {"name": "Fatigue Load Model 3 (One Vehicle)", "defaults": {"AMP": 1}},
                    {"name": "Fatigue Load Model 3 (Two Vehicle)", "defaults": {"AMP": 1, "INTERVAL": 31.6}},
                    {"name": "Fatigue Load Model 4 (200)", "defaults": {"AMP": 1}},
                    {"name": "Fatigue Load Model 4 (310)", "defaults": {"AMP": 1}},
                    {"name": "Fatigue Load Model 4 (490)", "defaults": {"AMP": 1}},
                    {"name": "Fatigue Load Model 4 (390)", "defaults": {"AMP": 1}},
                    {"name": "Fatigue Load Model 4 (450)", "defaults": {"AMP": 1}}
                ]
            },
            "RailTraffic": {
                "full_name": "EN 1991-2:2003-Rail Traffic Load", "sub_type": 23,
                "vehicle_types": [
                    {"name": "Load Model 71", "defaults": {"W1": 80, "DD1": 0, "D1": 0.8, "W2": 80, "DD2": 0, "D2": 0.8, "V_LOAD_FACTOR": 1, "LONGI_DIST": False, "ECCEN_VERT_LOAD": False}},
                    {"name": "Load Model SW/0", "defaults": {"W1": 133, "DD1": 15, "D1": 5.3, "W2": 133, "DD2": 15, "D2": 0, "V_LOAD_FACTOR": 1, "LONGI_DIST": False, "ECCEN_VERT_LOAD": False}},
                    {"name": "Load Model SW/2", "defaults": {"W1": 150, "DD1": 25, "D1": 7, "W2": 150, "DD2": 25, "D2": 0, "V_LOAD_FACTOR": 1, "LONGI_DIST": False, "ECCEN_VERT_LOAD": False}},
                    {"name": "Unloaded Train", "defaults": {"W1": 10, "DD1": 0, "D1": 0, "W2": 0, "DD2": 0, "D2": 0, "V_LOAD_FACTOR": 1, "LONGI_DIST": False, "ECCEN_VERT_LOAD": False}},
                    {"name": "HSLM B", "defaults": {"V_LOAD_FACTOR": 1, "LONGI_DIST": False, "ECCEN_VERT_LOAD": False, "HSLMB_NUM": 10, "HSLMB_FORCE": 170, "HSLMB_DIST": 3.5, "PHI_DYN_EFF1": 0, "PHI_DYN_EFF2": 0}},
                    {"name": "HSLM A1 ~ HSLM A10", "selectable_vehicles": [f"A{i}" for i in range(1, 11)], "defaults": {"V_LOAD_FACTOR": 1, "LONGI_DIST": False, "ECCEN_VERT_LOAD": False, "PHI_DYN_EFF1": 0, "PHI_DYN_EFF2": 0}}
                ]
            }
        }

        def __init__(self, code: str, v_type: str, name: str, id: int = None, **kwargs):
            """Base class for vehicle definition"""
            self.code, self.v_type, self.name = code, v_type, name
            self.id = len(MovingLoad.Vehicle.vehicles) + 1 if id is None else id
            self.params = kwargs
            if not any(v.id == self.id for v in MovingLoad.Vehicle.vehicles):
                MovingLoad.Vehicle.vehicles.append(self)
        #--------------------------------------------------------------- INDIA----------------------------------------------------
        class India:
            """
            Defines a Standard Indian Vehicle
            """
            def __init__(self,
                         name: str,
                         standard_code: str,
                         vehicle_type: str,
                         vehicle_name: int = None,
                         id: int = None):
                """
                    name (str): A unique name for the vehicle load.
                    standard_code (str): Abbreviation for the standard code ("IRC", "IRS", "Footway", "Fatigue").
                    vehicle_type (str): The specific type of vehicle.
                        - For "IRC": "Class A", "Class B", "Class 70R", "Class 40R", "Class AA","Footway".
                        - For "IRS": Use short codes: "BG-1676", "MG-1000", "NG-762", "HML", "FTB".
                    vehicle_name (int, optional): The numeric identifier (1-based) for the vehicle, required for "IRS" code.
                    id (int, optional): A unique ID for the vehicle. Auto-assigned if None.
                """
                code_map = {"IRC": "IRC:6-2000", "Footway": "IRC:6-2000", "IRS": "IRS: BRIDGE RULES", "Fatigue": "IRC:6-2014"}
                full_standard_code = code_map.get(standard_code)
                if not full_standard_code:
                    raise ValueError(f"Invalid standard_code. Use 'IRC', 'IRS', 'Footway', or 'Fatigue'.")

                all_params = { "standard_code": full_standard_code }
                defaults = {}

                if standard_code == "IRS":
                    if not vehicle_name:
                        raise ValueError("'vehicle_name' is required for IRS standard code.")
                    
                    irs_map = MovingLoad.Vehicle._irs_vehicle_map
                    if vehicle_type not in irs_map:
                        raise ValueError(f"Invalid IRS vehicle_type '{vehicle_type}'. Choose from {list(irs_map.keys())}")
                    
                    vehicle_info = irs_map[vehicle_type]
                    all_params["vehicle_type_name"] = vehicle_info["full_name"]
                    
                    if not (1 <= vehicle_name <= len(vehicle_info["vehicles"])):
                        raise ValueError(f"Invalid 'vehicle_name' {vehicle_name} for type '{vehicle_type}'. "
                                         f"Must be between 1 and {len(vehicle_info['vehicles'])}.")
                    
                    select_vehicle_name = vehicle_info["vehicles"][vehicle_name - 1]
                    all_params["select_vehicle"] = select_vehicle_name

                    # Get defaults for the specific IRS vehicle
                    if vehicle_type in MovingLoad.Vehicle._india_defaults_map["IRS"]:
                        if select_vehicle_name in MovingLoad.Vehicle._india_defaults_map["IRS"][vehicle_type]:
                            defaults = MovingLoad.Vehicle._india_defaults_map["IRS"][vehicle_type][select_vehicle_name]
                
                else: # For IRC, Footway, Fatigue
                    all_params["vehicle_type_name"] = vehicle_type
                    # Get defaults if any exist for this type
                    if standard_code in MovingLoad.Vehicle._india_defaults_map:
                         if vehicle_type in MovingLoad.Vehicle._india_defaults_map[standard_code]:
                            defaults = MovingLoad.Vehicle._india_defaults_map[standard_code][vehicle_type]

                all_params.update(defaults)
                MovingLoad.Vehicle("INDIA", "Standard", name, id, **all_params)
        
        class Eurocode:
            """
            Defines a Standard Eurocode Vehicle
            """
            def __init__(self,
                         name: str,
                         standard_code: str,
                         vehicle_type: str,
                         vehicle_name: int = None,
                         id: int = None):
                """
                    name (str): A unique name for the vehicle load.
                    standard_code (str): Abbreviation for the standard code.
                        - "RoadBridge", "FTB", "RoadBridgeFatigue", "RailTraffic"
                    vehicle_type (str): The specific type of vehicle (e.g., "Load Model 1", "Load Model 3").
                    vehicle_name (int, optional): The numeric ID (1-based) for a selectable vehicle (e.g., for "Load Model 3").
                    id (int, optional): A unique ID for the vehicle. Auto-assigned if None.
                """
                euro_map = MovingLoad.Vehicle._euro_vehicle_map
                if standard_code not in euro_map:
                    raise ValueError(f"Invalid standard_code. Choose from {list(euro_map.keys())}")
                
                std_info = euro_map[standard_code]
                v_type_info = next((vt for vt in std_info["vehicle_types"] if vt["name"] == vehicle_type), None)
                if not v_type_info:
                    available_types = [vt['name'] for vt in std_info['vehicle_types']]
                    raise ValueError(f"Invalid vehicle_type '{vehicle_type}' for '{standard_code}'. Choose from: {available_types}")

                # Start with the default parameters for the vehicle type
                all_params = v_type_info.get("defaults", {}).copy()
                all_params["SUB_TYPE"] = std_info["sub_type"]
                all_params["vehicle_type_name"] = vehicle_type

                # Handle selectable vehicles
                if "selectable_vehicles" in v_type_info:
                    if not vehicle_name:
                        raise ValueError(f"'vehicle_name' is required for vehicle_type '{vehicle_type}'.")
                    selectable_list = v_type_info["selectable_vehicles"]
                    if not (1 <= vehicle_name <= len(selectable_list)):
                        raise ValueError(f"Invalid 'vehicle_name' {vehicle_name} for type '{vehicle_type}'. Must be between 1 and {len(selectable_list)}.")
                    
                    select_vehicle_name = selectable_list[vehicle_name - 1]
                    all_params["SEL_VEHICLE"] = select_vehicle_name
                
                MovingLoad.Vehicle("EUROCODE", "Standard", name, id, **all_params)

        @classmethod
        def create(cls):
            """Sends all defined vehicle data to the Midas Civil"""
            if not cls.vehicles: 
                print("No vehicles defined to create.")
                return
            
            json_data = cls.json(cls.vehicles)
            MidasAPI("PUT", "/db/mvhl", json_data)


        @classmethod
        def json(cls, vehicle_list=None):
            """
            Generates the JSON Data
            """
            if vehicle_list is None:
                vehicle_list = cls.vehicles

            data = {"Assign": {}}
            for v in vehicle_list:
                # Creates a copy to avoid modifying the original stored parameters
                params = v.params.copy()
                
                if v.code == "INDIA":
                    vehicle_data = {
                        "MVLD_CODE": 7,  # Static code for INDIA
                        "VEHICLE_LOAD_NAME": v.name,
                        "VEHICLE_LOAD_NUM": 1, # Always Standard for this implementation
                        "STANDARD_CODE": params.pop("standard_code"),
                        "VEHICLE_TYPE_NAME": params.pop("vehicle_type_name")
                    }
                    
                    # Extract the selected vehicle name if it exists
                    select_vehicle_name = params.pop("select_vehicle", None)
                    
                    # The remaining parameters in 'params' should be the content for VEH_IN
                    # If VEH_IN was added from defaults, use it
                    if "VEH_IN" in params:
                        # For IRS vehicles, SEL_VEHICLE key is required inside the VEH_IN block
                        if select_vehicle_name:
                            params["VEH_IN"]["SEL_VEHICLE"] = select_vehicle_name
                        vehicle_data["VEH_IN"] = params["VEH_IN"]
                    # If there's no default VEH_IN but a vehicle name is selected (e.g., basic IRC class)
                    elif select_vehicle_name:
                        vehicle_data["VEH_IN"] = {"SEL_VEHICLE": select_vehicle_name}
                    
                    data["Assign"][str(v.id)] = vehicle_data

                elif v.code == "EUROCODE":
                    vehicle_data = {
                        "MVLD_CODE": 11, # Static code for EUROCODE
                        "VEHICLE_LOAD_NAME": v.name,
                        "VEHICLE_LOAD_NUM": 1, # Always Standard for this implementation
                        "VEHICLE_TYPE_NAME": params.pop("vehicle_type_name"),
                        # All other parameters are nested under VEH_EUROCODE
                        "VEH_EUROCODE": params 
                    }
                    data["Assign"][str(v.id)] = vehicle_data
            
            return data

        @classmethod
        def sync(cls):
            """
            Synchronizes the vehicle data from the Midas model 
            """
            cls.vehicles = []  # Clear the local list before syncing
            response = cls.get()

            if not response or "MVHL" not in response:
                print("No vehicle data found in the model to sync.")
                return

            all_vehicles_data = response["MVHL"]

            # --- Reverse Maps for Lookups ---
            # India Standard Code (e.g., "IRC:6-2000" -> "IRC")
            india_std_code_rev_map = {
                "IRC:6-2000": "IRC",
                "IRS: BRIDGE RULES": "IRS",
                "IRC:6-2014": "Fatigue"
            }
            # India Vehicle Type (e.g., "Broad Gauge-1676mm" -> "BG-1676")
            india_type_rev_map = {v['full_name']: k for k, v in cls._irs_vehicle_map.items()}

            # Eurocode Standard Code (e.g., 19 -> "RoadBridge")
            euro_std_code_rev_map = {v['sub_type']: k for k, v in cls._euro_vehicle_map.items()}


            for v_id, v_data in all_vehicles_data.items():
                vehicle_id = int(v_id)
                mvld_code = v_data.get("MVLD_CODE")
                vehicle_load_name = v_data.get("VEHICLE_LOAD_NAME")

                # --- Sync logic for INDIA vehicles ---
                if mvld_code == 7:
                    standard_code_full = v_data.get("STANDARD_CODE")
                    vehicle_type_full = v_data.get("VEHICLE_TYPE_NAME")
                    
                    # Handle special case for Footway which uses IRC standard
                    if vehicle_type_full == "Footway":
                        standard_code = "Footway"
                        vehicle_type = "Footway"
                        vehicle_name_id = None
                    else:
                        standard_code = india_std_code_rev_map.get(standard_code_full)
                        vehicle_type = india_type_rev_map.get(vehicle_type_full)
                        vehicle_name_id = None
                    
                    if standard_code == "IRS" and "VEH_IN" in v_data:
                        sel_vehicle_name = v_data["VEH_IN"].get("SEL_VEHICLE")
                        if vehicle_type in cls._irs_vehicle_map and sel_vehicle_name:
                            try:
                                # Find the 1-based index of the vehicle name
                                vehicle_name_id = cls._irs_vehicle_map[vehicle_type]["vehicles"].index(sel_vehicle_name) + 1
                            except ValueError:
                                print(f"Warning: Could not find vehicle name '{sel_vehicle_name}' for type '{vehicle_type}' during sync.")
                                continue
                    
                    # Instantiate the vehicle to add it to the local list
                    MovingLoad.Vehicle.India(
                        name=vehicle_load_name,
                        standard_code=standard_code,
                        vehicle_type=vehicle_type or vehicle_type_full, # Fallback to full name if no short code
                        vehicle_name=vehicle_name_id,
                        id=vehicle_id
                    )

                # --- Sync logic for EUROCODE vehicles ---
                elif mvld_code == 11 and "VEH_EUROCODE" in v_data:
                    euro_params = v_data["VEH_EUROCODE"]
                    sub_type = euro_params.get("SUB_TYPE")
                    vehicle_type_name = v_data.get("VEHICLE_TYPE_NAME")

                    standard_code = euro_std_code_rev_map.get(sub_type)
                    if not standard_code:
                        print(f"Warning: Unknown Eurocode SUB_TYPE '{sub_type}' for vehicle ID {vehicle_id}. Skipping.")
                        continue
                    
                    # Check if this vehicle type has selectable options
                    std_info = cls._euro_vehicle_map.get(standard_code, {})
                    v_type_info = next((vt for vt in std_info.get("vehicle_types", []) if vt["name"] == vehicle_type_name), None)
                    
                    vehicle_name_id = None
                    if v_type_info and "selectable_vehicles" in v_type_info:
                        sel_vehicle_name = euro_params.get("SEL_VEHICLE")
                        if sel_vehicle_name:
                            try:
                                vehicle_name_id = v_type_info["selectable_vehicles"].index(sel_vehicle_name) + 1
                            except ValueError:
                                print(f"Warning: Could not find Eurocode vehicle name '{sel_vehicle_name}' for type '{vehicle_type_name}' during sync.")
                                continue
                    
                    MovingLoad.Vehicle.Eurocode(
                        name=vehicle_load_name,
                        standard_code=standard_code,
                        vehicle_type=vehicle_type_name,
                        vehicle_name=vehicle_name_id,
                        id=vehicle_id
                    )

        @classmethod
        def get(cls):
            """Gets all vehicle load definitions from the Midas model."""
            return MidasAPI("GET", "/db/mvhl")
        

        
        @classmethod
        def delete(cls):
            """Deletes all vehicles from the Midas model."""
            return MidasAPI("DELETE", "/db/mvhl")


#--------------------------------------------------Load Case--------------------------------------------

    class Case:
        
        cases = []

        def __init__(self, code: str, case_id: int, params: dict):
            """
            Internal constructor for the Case class. User should use country-specific subclasses.
            """
            self.code = code
            self.id = case_id
            self.params = params
            
            # Add the new case instance to the class-level list, avoiding duplicates by ID
            if not any(c.id == self.id for c in self.__class__.cases):
                self.__class__.cases.append(self)

        @classmethod
        def create(cls):
            """
            Creates moving load cases in the Midas model for all defined country codes.
            """
            if not cls.cases:
                print("No moving load cases to create.")
                return
            
            # Separate cases by country code and send them to the appropriate API endpoint
            country_codes = set(c.code for c in cls.cases)
            for code in country_codes:
                cases_to_create = [c for c in cls.cases if c.code == code]
                if cases_to_create:
                    json_data = cls.json(cases_to_create)
                    endpoint = ""
                    if code == "INDIA":
                        endpoint = "/db/MVLDid"
                    elif code == "EUROCODE":
                        endpoint = "/db/MVLDeu"
                    
                    if endpoint:
                        MidasAPI("PUT", endpoint, json_data)
            
            # Clear the list after creation
            cls.cases.clear()

        @classmethod
        def json(cls, case_list=None):
            """Generates the JSON for a list of cases. Uses all stored cases if list is not provided."""
            if case_list is None:
                case_list = cls.cases
            data = {"Assign": {}}
            for case in case_list:
                data["Assign"][str(case.id)] = case.params
            return data

        @classmethod
        def get(cls):
            """
            Retrieves all moving load cases from the Midas model 
            """
            all_cases_data = {}
            
            # Define endpoints and their expected response keys.
            endpoints = {
                "/db/MVLDid": "MVLDID",
                "/db/MVLDeu": "MVLDEU"
            }

            for endpoint, response_key in endpoints.items():
                api_data = MidasAPI("GET", endpoint)
                
                # Check if the response is valid and contains the expected key
                if api_data and response_key in api_data:
                    # Add the data under its original API key (e.g., "MVLDID")
                    all_cases_data[response_key] = api_data[response_key]
            
            return all_cases_data

        @classmethod
        def delete(cls):
            """Deletes all moving load cases from the Midas model."""
            all_cases_in_model = cls.get()
            if not all_cases_in_model:
                return

            if "MVLDID" in all_cases_in_model:
                MidasAPI("DELETE", "/db/MVLDid")
            if "MVLDEU" in all_cases_in_model:
                MidasAPI("DELETE", "/db/MVLDeu")

        @classmethod
        def sync(cls):
            """
            Synchronizes the load case data from the Midas model 
            """
            cls.cases = []
            response = cls.get()

            # Sync India Cases
            if "MVLDID" in response:
                for case_id, case_data in response["MVLDID"].items():
                    name = case_data.get("LCNAME")
                    num_lanes = case_data.get("NUM_LOADED_LANES")
                    scale_factor = case_data.get("SCALE_FACTOR")

                    # Case 1: Permit Vehicle Load
                    if case_data.get("OPT_LC_FOR_PERMIT_LOAD"):
                        MovingLoad.Case.India(
                            id=int(case_id),
                            name=name,
                            num_loaded_lanes=num_lanes,
                            scale_factor=scale_factor,
                            opt_lc_for_permit=True,
                            permit_vehicle_id=case_data.get("PERMIT_VEHICLE"),
                            ref_lane_id=case_data.get("REF_LANE"),
                            eccentricity=case_data.get("ECCEN"),
                            permit_scale_factor=case_data.get("PERMIT_SCALE_FACTOR")
                        )
                    # Case 2: Auto Live Load Combination
                    elif case_data.get("OPT_AUTO_LL"):
                        sub_items = []
                        for item in case_data.get("SUB_LOAD_ITEMS", []):
                            sub_items.append([
                                item.get("SCALE_FACTOR"),
                                item.get("VEHICLE_CLASS_1"),
                                item.get("VEHICLE_CLASS_2"),
                                item.get("FOOTWAY"),
                                item.get("SELECTED_LANES"),
                                item.get("SELECTED_FOOTWAY_LANES") # Will be None if not present
                            ])
                        MovingLoad.Case.India(
                            id=int(case_id),
                            name=name,
                            num_loaded_lanes=num_lanes,
                            scale_factor=scale_factor,
                            opt_auto_ll=True,
                            sub_load_items=sub_items
                        )
                    # Case 3: General Load
                    else:
                        sub_items = []
                        for item in case_data.get("SUB_LOAD_ITEMS", []):
                            sub_items.append([
                                item.get("SCALE_FACTOR"),
                                item.get("MIN_NUM_LOADED_LANES"),
                                item.get("MAX_NUM_LOADED_LANES"),
                                item.get("VEHICLE_CLASS_1"),
                                item.get("SELECTED_LANES")
                            ])
                        MovingLoad.Case.India(
                            id=int(case_id),
                            name=name,
                            num_loaded_lanes=num_lanes,
                            scale_factor=scale_factor,
                            opt_auto_ll=False,
                            sub_load_items=sub_items
                        )

            # Sync Eurocode Cases
            if "MVLDEU" in response:
                for case_id, case_data in response["MVLDEU"].items():
                    # The Eurocode constructor can handle the raw dictionary via **kwargs
                    # by leveraging its fallback mechanism when sub_load_items is not provided.
                    name = case_data.pop("LCNAME")
                    load_model = case_data.pop("TYPE_LOADMODEL")
                    use_optimization = case_data.pop("OPT_AUTO_OPTIMIZE")
                    
                    MovingLoad.Case.Eurocode(
                        id=int(case_id),
                        name=name,
                        load_model=load_model,
                        use_optimization=use_optimization,
                        **case_data  # Pass the rest of the data as keyword arguments
                    )

        class India:
            """
            Defines a Moving Load Case according to Indian standards.
           
            """
            def __init__(self,
                        name: str,
                        num_loaded_lanes: int,
                        id: int = None,
                        # --- Switches to select the type of load case ---
                        opt_auto_ll: bool = False,
                        opt_lc_for_permit: bool = False,
                        
                        # --- Common and General Load Parameters ---
                        sub_load_items: list = None,
                        scale_factor: list = None,

                        # --- Permit Vehicle Specific Parameters ---
                        permit_vehicle_id: int = None,
                        ref_lane_id: int = None,
                        eccentricity: float = None,
                        permit_scale_factor: float = None):
                """
               
                    name (str): The name of the load case (LCNAME).
                    num_loaded_lanes (int): The number of loaded lanes.
                    id (int, optional): A unique integer ID for the case.
                    opt_auto_ll (bool, optional): Set to True for "Auto Live Load Combinations".
                    opt_lc_for_permit (bool, optional): Set to True for "Load Cases for Permit Vehicle".
                    sub_load_items (list, optional): A list of lists defining sub-loads. The format depends on the selected options:

                        *** Case 1: General Load Format (opt_auto_ll=False) ***
                        Each inner list must contain 5 items in this order:
                        1. Scale Factor (Number)
                        2. Min. Number of Loaded Lanes (Integer)
                        3. Max. Number of Loaded Lanes (Integer)
                        4. Vehicle Name (String, e.g., "Class A")
                        5. Selected Lanes (list[str], e.g., ["T1", "T2"])

                        *** Case 2: Auto Live Load Format (opt_auto_ll=True) ***
                        Each inner list must contain 5-6 items in this order:
                        1. Scale Factor (Number)
                        2. Vehicle Class I (String)
                        3. Vehicle Class II (String)
                        4. Vehicle Footway (String, "" for none)
                        5. Selected Carriageway Lanes (list[str])
                        6. Selected Footway Lanes (list[str]) - Optional, omit or set to None if no footway.

                        *** Case 3: Permit Vehicle Format (opt_lc_for_permit=True) ***
                        sub_load_items is not used. Use permit_vehicle_id, ref_lane_id, etc. instead.

                    scale_factor (list, optional): A list of 4 numbers for the Multiple Presence Factor. Defaults to [1, 0.9, 0.8, 0.8].
                    permit_vehicle_id (int, optional): The ID of the permit vehicle. Required for permit cases.
                    ref_lane_id (int, optional): The reference lane ID. Required for permit cases.
                    eccentricity (float, optional): Eccentricity for the permit vehicle. Required for permit cases.
                    permit_scale_factor (float, optional): Scale factor for the permit vehicle. Required for permit cases.
                """
                if id is None:
                    # Correctly reference the 'cases' list through its full path
                    case_id = (max(c.id for c in MovingLoad.Case.cases) + 1) if MovingLoad.Case.cases else 1
                else:
                    case_id = id
                final_scale_factor = scale_factor if scale_factor is not None else [1, 0.9, 0.8, 0.8]

                params = {
                    "LCNAME": name,
                    "DESC": "",
                    "SCALE_FACTOR": final_scale_factor,
                    "NUM_LOADED_LANES": num_loaded_lanes
                }
                
                formatted_sub_loads = []

                if opt_lc_for_permit:
                    if any(p is None for p in [permit_vehicle_id, ref_lane_id, eccentricity, permit_scale_factor]):
                        raise ValueError("For Permit Vehicle cases, 'permit_vehicle_id', 'ref_lane_id', 'eccentricity', and 'permit_scale_factor' are required.")
                    
                    params.update({
                        "OPT_AUTO_LL": True,
                        "OPT_LC_FOR_PERMIT_LOAD": True,
                        "PERMIT_VEHICLE": permit_vehicle_id,
                        "REF_LANE": ref_lane_id,
                        "ECCEN": eccentricity,
                        "PERMIT_SCALE_FACTOR": permit_scale_factor
                    })

                elif opt_auto_ll:
                    if sub_load_items is None:
                        raise ValueError("For Auto Live Load cases, 'sub_load_items' is required.")
                    
                    carriage_way_width = 2.3 if num_loaded_lanes == 1 else 0
                    carriage_way_loading = 4.903325 if num_loaded_lanes == 1 else 0
                    
                    for item_list in sub_load_items:
                        sub_load_dict = {
                            "SCALE_FACTOR": item_list[0],
                            "VEHICLE_CLASS_1": item_list[1],
                            "VEHICLE_CLASS_2": item_list[2],
                            "FOOTWAY": item_list[3],
                            "CARRIAGE_WAY_WIDTH": carriage_way_width,
                            "CARRIAGE_WAY_LOADING": carriage_way_loading,
                            "SELECTED_LANES": item_list[4]
                        }
                        if len(item_list) > 5 and item_list[5] is not None:
                            sub_load_dict["SELECTED_FOOTWAY_LANES"] = item_list[5]
                        formatted_sub_loads.append(sub_load_dict)
                    
                    params.update({
                        "OPT_AUTO_LL": True,
                        "OPT_LC_FOR_PERMIT_LOAD": False,
                        "SUB_LOAD_ITEMS": formatted_sub_loads
                    })
                
                else: # General Load
                    if sub_load_items is None:
                        raise ValueError("For General Load cases, 'sub_load_items' is required.")
                    
                    for item_list in sub_load_items:
                        formatted_sub_loads.append({
                            "SCALE_FACTOR": item_list[0],
                            "MIN_NUM_LOADED_LANES": item_list[1],
                            "MAX_NUM_LOADED_LANES": item_list[2],
                            "VEHICLE_CLASS_1": item_list[3],
                            "SELECTED_LANES": item_list[4]
                        })

                    params.update({
                        "OPT_AUTO_LL": False,
                        "OPT_LC_FOR_PERMIT_LOAD": False,
                        "SUB_LOAD_ITEMS": formatted_sub_loads
                    })

                MovingLoad.Case("INDIA", case_id, params)

        class Eurocode:
            
            def __init__(self,
                        name: str,
                        load_model: int,
                        use_optimization: bool = False,
                        id: int = None,
                        sub_load_items: list = None,
                        **kwargs):
                """
                
                    name (str): The name of the load case (LCNAME).
                    load_model (int): The Eurocode Load Model type (1-5).
                    use_optimization (bool, optional): Set to True for "Moving Load Optimization". Defaults to False.
                    id (int, optional): A unique integer ID for the case. Auto-assigned if None.
                    sub_load_items (list, optional): Simplified list input. Format depends on the load_model and use_optimization.
                    **kwargs: Additional individual parameters (for backward compatibility).

                * General Load (use_optimization=False) *

                - load_model = 1: [opt_leading, vhl_name1, vhl_name2, selected_lanes, remaining_area, footway_lanes]
                Example: [False, "V1", "V2", ["L1"], ["L2"], ["F1"]]

                - load_model = 2: [opt_leading, opt_comb, [(name, sf, min_L, max_L, [lanes]), ...]]
                Example: [True, 1, [("V_Permit", 1.0, 1, 4, ["L1", "L2"])]]

                - load_model = 3: [opt_leading, vhl_name1, vhl_name2, selected_lanes, remaining_area]
                Example: [False, "V1", "V3", ["L1", "L2"], ["L3"]]

                - load_model = 4: [opt_leading, vhl_name1, vhl_name2, selected_lanes, remaining_area, straddling_lanes]
                Where straddling_lanes is a list of dicts: [{'NAME1': 'start', 'NAME2': 'end'}, ...]
                Example: [False, "V1", "V4", ["L1"], ["L2"], [{"NAME1": "L3", "NAME2": "L4"}]]

                - load_model = 5 (Railway): [opt_psi, opt_comb, [sf1,sf2,sf3], [mf1,mf2,mf3], [(name, sf, min_L, max_L, [lanes]), ...]]
                Example: [False, 1, [0.8,0.7,0.6], [1,1,0.75], [("Rail-V", 1, 1, 1, ["T1"])]]

                * Moving Load Optimization (use_optimization=True) *

                - load_model = 1: [opt_leading, vhl_name1, vhl_name2, min_dist, opt_lane, loaded_lanes, [selected_lanes]]
                Example: [False, "V1", "V2", 10, "L1", 2, ["L1", "L2"]]

                - load_model = 2: [opt_leading, opt_comb, min_dist, opt_lane, min_v, max_v, [(name, sf), ...]]
                Example: [False, 1, 10, "L1", 1, 2, [("V_Permit", 1.0), ("V_Other", 0.8)]]

                - load_model = 3: [opt_leading, vhl_name1, vhl_name2, min_dist, opt_lane, loaded_lanes, [selected_lanes]]
                Example: [True, "V1", "V3_auto", 10, "L1", 3, ["L1", "L2", "L3"]]

                - load_model = 4: [opt_leading, vhl_name1, vhl_name2, min_dist, opt_lane, loaded_lanes, [selected_lanes], [straddling_lanes]]
                Example: [True, "V1", "V4_auto", 10, "L2", 3, ["L1", "L3"], [{"NAME1": "L3", "NAME2": "L4"}]]

                - load_model = 5 (Railway): [opt_psi, opt_comb, [sf1,sf2,sf3], [mf1,mf2,mf3], min_dist, opt_lane, min_v, max_v, [(name, sf), ...]]
                Example: [False, 1, [0.8,0.7,0.6], [1,1,0.75], 20, "T1", 1, 1, [("Rail-V", 1)]]
                """
                if id is None:
                    # Correctly reference the 'cases' list through its full path
                    case_id = (max(c.id for c in MovingLoad.Case.cases) + 1) if MovingLoad.Case.cases else 1
                else:
                    case_id = id
                params = {
                    "LCNAME": name,
                    "DESC": kwargs.get("DESC", ""),
                    "TYPE_LOADMODEL": load_model,
                    "OPT_AUTO_OPTIMIZE": use_optimization
                }

                if sub_load_items is None:
                    # Fallback to kwargs for backward compatibility if sub_load_items is not used
                    params.update(kwargs)
                    MovingLoad.Case("EUROCODE", case_id, params)
                    return

                if not use_optimization:  # General Load
                    if load_model == 1:
                        params.update({"OPT_LEADING": sub_load_items[0], "VHLNAME1": sub_load_items[1], "VHLNAME2": sub_load_items[2], "SLN_LIST": sub_load_items[3], "SRA_LIST": sub_load_items[4], "FLN_LIST": sub_load_items[5]})
                    elif load_model == 2:
                        sub_loads = [{"TYPE": 2, "NAME": item[0], "SCALE_FACTOR": item[1], "MIN_LOAD_LANE_TYPE": item[2], "MAX_LOAD_LANE_TYPE": item[3], "SLN_LIST": item[4]} for item in sub_load_items[2]]
                        params.update({"OPT_LEADING": sub_load_items[0], "OPT_COMB": sub_load_items[1], "SUB_LOAD_LIST": sub_loads})
                    elif load_model == 3:
                        params.update({"OPT_LEADING": sub_load_items[0], "VHLNAME1": sub_load_items[1], "VHLNAME2": sub_load_items[2], "SLN_LIST": sub_load_items[3], "SRA_LIST": sub_load_items[4]})
                    elif load_model == 4:
                        params.update({"OPT_LEADING": sub_load_items[0], "VHLNAME1": sub_load_items[1], "VHLNAME2": sub_load_items[2], "SLN_LIST": sub_load_items[3], "SRA_LIST": sub_load_items[4], "STL_LIST": sub_load_items[5]})
                    elif load_model == 5:
                        sub_loads = [{"TYPE": 2, "NAME": item[0], "SCALE_FACTOR": item[1], "MIN_LOAD_LANE_TYPE": item[2], "MAX_LOAD_LANE_TYPE": item[3], "SLN_LIST": item[4]} for item in sub_load_items[4]]
                        params.update({"OPT_PSI_FACTOR": sub_load_items[0], "OPT_COMB": sub_load_items[1], "SCALE_FACTOR1": sub_load_items[2][0], "SCALE_FACTOR2": sub_load_items[2][1], "SCALE_FACTOR3": sub_load_items[2][2], "MULTI_FACTOR1": sub_load_items[3][0], "MULTI_FACTOR2": sub_load_items[3][1], "MULTI_FACTOR3": sub_load_items[3][2], "SUB_LOAD_LIST": sub_loads})
                
                else:  # Moving Load Optimization
                    if load_model == 1:
                        params.update({"OPT_LEADING": sub_load_items[0], "VHLNAME1": sub_load_items[1], "VHLNAME2": sub_load_items[2], "MINVHLDIST": sub_load_items[3], "OPTIMIZE_LANE_NAME": sub_load_items[4], "LOADEDLANE": sub_load_items[5], "SLN_LIST": sub_load_items[6]})
                    elif load_model == 2:
                        opt_list = [{"TYPE": 2, "NAME": item[0], "SCALE_FACTOR": item[1]} for item in sub_load_items[6]]
                        params.update({"OPT_LEADING": sub_load_items[0], "OPT_COMB": sub_load_items[1], "MINVHLDIST": sub_load_items[2], "OPTIMIZE_LANE_NAME": sub_load_items[3], "MIN_NUM_VHL": sub_load_items[4], "MAX_NUM_VHL": sub_load_items[5], "OPTIMIZE_LIST": opt_list})
                    elif load_model == 3:
                        params.update({"OPT_LEADING": sub_load_items[0], "VHLNAME1": sub_load_items[1], "VHLNAME2": sub_load_items[2], "MINVHLDIST": sub_load_items[3], "OPTIMIZE_LANE_NAME": sub_load_items[4], "LOADEDLANE": sub_load_items[5], "SLN_LIST": sub_load_items[6]})
                    elif load_model == 4:
                        params.update({"OPT_LEADING": sub_load_items[0], "VHLNAME1": sub_load_items[1], "VHLNAME2": sub_load_items[2], "MINVHLDIST": sub_load_items[3], "OPTIMIZE_LANE_NAME": sub_load_items[4], "LOADEDLANE": sub_load_items[5], "SLN_LIST": sub_load_items[6], "STL_LIST": sub_load_items[7]})
                    elif load_model == 5:
                        opt_list = [{"TYPE": 2, "NAME": item[0], "SCALE_FACTOR": item[1]} for item in sub_load_items[8]]
                        params.update({"OPT_PSI_FACTOR": sub_load_items[0], "OPT_COMB": sub_load_items[1], "SCALE_FACTOR1": sub_load_items[2][0], "SCALE_FACTOR2": sub_load_items[2][1], "SCALE_FACTOR3": sub_load_items[2][2], "MULTI_FACTOR1": sub_load_items[3][0], "MULTI_FACTOR2": sub_load_items[3][1], "MULTI_FACTOR3": sub_load_items[3][2], "MINVHLDIST": sub_load_items[4], "OPTIMIZE_LANE_NAME": sub_load_items[5], "MIN_NUM_VHL": sub_load_items[6], "MAX_NUM_VHL": sub_load_items[7], "OPTIMIZE_LIST": opt_list})

                MovingLoad.Case("EUROCODE", case_id, params)



    #--------------------------------------Test---------------------------------------------