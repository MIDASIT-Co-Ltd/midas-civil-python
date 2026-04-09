from ._offsetSS import Offset
from ._offsetSS import _common
from math import sin,cos,pi

class _SS_TAPERED_DBUSER(_common):
    """Tapered user-defined standard section for MIDAS Civil NX.

    Represents a tapered section whose cross-section varies linearly from the
    I-end (start) to the J-end (end) of a frame element. The shape type and
    dimension parameters are shared across both ends; only the sizes differ.

    Supported shapes (``Shape`` argument):
        - ``'SB'`` : Solid rectangle — params ``[H, B]``
        - ``'L'``  : Angle (L-section) — params ``[H, B, tw, tf]``
        - ``'C'``  : Channel — params ``[H, B1, tw, tf1, B2, tf2]``
        - ``'H'``  : H-beam / I-beam — params ``[H, B1, tw, tf1, B2, tf2, r1, r2]``
        - ``'T'``  : T-section — params ``[H, B, tw, tf]``
        - ``'B'``  : Box section — params ``[H, B, tw, tf1, C, tf2]``
        - ``'P'``  : Pipe (hollow circle) — params ``[D, tw]``

    Attributes:
        ID (int): Section database ID assigned by MIDAS.
        NAME (str): Section name.
        TYPE (str): Always ``'TAPERED'``.
        SHAPE (str): Shape code (see above).
        PARAMS_I (list[float]): Dimension parameters at the I-end.
        PARAMS_J (list[float]): Dimension parameters at the J-end.
        OFFSET (Offset): Cross-section offset configuration.
        USESHEAR (bool): Whether to include shear deformation.
        USE7DOF (bool): Whether to include warping (7th DOF) effect.
        DATATYPE (int): Internal MIDAS data-type identifier (always ``2``).
    """

    def __init__(self, Name='', Shape='', params_I: list = [], params_J: list = [],
                 Offset=Offset(), useShear=True, use7Dof=False, id: int = 0):
        """Initialise a tapered user-defined section.

        Args:
            Name (str): Section name as it will appear in the MIDAS model.
            Shape (str): Shape code. One of ``'SB'``, ``'L'``, ``'C'``, ``'H'``,
                ``'T'``, ``'B'``, or ``'P'``.
            params_I (list[float]): Dimension parameters at the I-end of the
                element. Order depends on the chosen shape (see class docstring).
            params_J (list[float]): Dimension parameters at the J-end of the
                element. Must use the same ordering as ``params_I``.
            Offset (Offset): Section offset object controlling the reference
                point and horizontal/vertical offsets. Defaults to centroid (CC).
            useShear (bool): Include shear deformation in the analysis.
                Defaults to ``True``.
            use7Dof (bool): Include warping (7th DOF / torsional warping) effect.
                Defaults to ``False``.
            id (int): Section ID in the MIDAS database. Assigned automatically
                when the section is pushed to the model; leave as ``0`` when
                creating a new section.
        """
        self.ID = id
        self.NAME = Name
        self.TYPE = 'TAPERED'
        self.SHAPE = Shape
        self.PARAMS_I = params_I
        self.PARAMS_J = params_J
        self.OFFSET = Offset
        self.USESHEAR = useShear
        self.USE7DOF = use7Dof
        self.DATATYPE = 2

    def __str__(self):
         return f'  >  ID = {self.ID}   |  USER DEFINED STANDARD SECTION \nJSON = {self.toJSON()}\n'


    def toJSON(sect):
        """Serialise the section to the MIDAS Civil NX API JSON format.

        Returns:
            dict: A dictionary ready to be sent to the ``/db/sect`` endpoint,
            containing the section type, name, shape, I/J parameters, offset
            settings, and analysis flags.
        """
        js =  {
                "SECTTYPE": sect.TYPE,
                "SECT_NAME": sect.NAME,
                "SECT_BEFORE": {
                    "SHAPE": sect.SHAPE,
                    "TYPE": sect.DATATYPE,
                    "SECT_I": {
                        "vSIZE": sect.PARAMS_I
                    },
                    "SECT_J": {
                        "vSIZE": sect.PARAMS_J
                    }
                }
            }
        js['SECT_BEFORE'].update(sect.OFFSET.JS)
        js['SECT_BEFORE']['USE_SHEAR_DEFORM'] = sect.USESHEAR
        js['SECT_BEFORE']['USE_WARPING_EFFECT'] = sect.USE7DOF
        return js

    @staticmethod
    def _objectify(id, name, type, shape, offset, uShear, u7DOF, js):
        """Reconstruct a ``_SS_TAPERED_DBUSER`` instance from raw API JSON.

        Args:
            id (int): Section database ID.
            name (str): Section name.
            type (str): Section type string (unused; always ``'TAPERED'``).
            shape (str): Shape code.
            offset (Offset): Offset object.
            uShear (bool): Shear deformation flag.
            u7DOF (bool): Warping effect flag.
            js (dict): Raw JSON dictionary from the ``/db/sect`` endpoint,
                containing ``SECT_BEFORE.SECT_I.vSIZE`` and
                ``SECT_BEFORE.SECT_J.vSIZE``.

        Returns:
            _SS_TAPERED_DBUSER: Reconstructed section object.
        """
        return _SS_TAPERED_DBUSER(name, shape, js['SECT_BEFORE']['SECT_I']['vSIZE'], js['SECT_BEFORE']['SECT_J']['vSIZE'], offset, uShear, u7DOF, id)

    def _centerLine(shape, end, *args):
        """Compute the wireframe geometry used to render the section outline.

        Selects either the I-end or J-end parameters and returns the geometric
        primitives required to draw a thin-wall centerline representation of
        the cross-section.

        Args:
            shape: The section object (used as ``self``).
            end (bool): ``True`` to use J-end parameters; ``False`` for I-end.
            *args: Reserved for future use.

        Returns:
            tuple:
                - **sect_shape** (list[list[float]]): Node coordinates
                  ``[y, z]`` of the section outline.
                - **sect_thk** (list[float]): Wall thickness at each segment.
                - **sect_thk_off** (list[float]): Thickness offset for each
                  segment (positive = outward from centreline).
                - **sect_cg** (tuple): Three reference points
                  ``(top-left, centroid, bottom-right)`` each as ``[y, z]``.
                - **sect_lin_con** (list[list[int]]): 1-based node connectivity
                  pairs ``[start, end]`` defining each wall segment.
        """
        if end:
            shape.PARAMS = shape.PARAMS_J
            # print(' J end taken')
        else:
            # print(' I end taken')
            shape.PARAMS = shape.PARAMS_I

        if shape.SHAPE == 'SB' :
            H,B = shape.PARAMS[:2]

            sect_lin_con = [[1,2],[3,1]]

            sect_cg_LT = [-B/2,H/2]
            sect_cg_CC = [0,0]
            sect_cg_RB = [B/2,-H/2]

            if H > B :
                sect_shape = [[0,0],[0,H/2],[0,-H/2],[0,H/4],[0,-H/4]]
                sect_thk = [B,B,B,B]
                sect_thk_off = [0,0,0,0]
            else : 
                sect_shape = [[0,0],[B/2,0],[-B/2,0],[B/4,0],[-B/4,0]]
                sect_thk = [H,H,H,H]
                sect_thk_off = [0,0,0,0]

        elif shape.SHAPE == 'L' :
            H,B,tw,tf = shape.PARAMS[:4]

            sect_cg_LT = [0,0]
            sect_cg_CC = [(H*tw*tw+B*B*tf)/(2*(B*tw+H*tf)),-(H*H*tw+B*tf*tf)/(2*(B*tw+H*tf))]
            sect_cg_RB = [B,-H]

            # sect_shape = [[0.5*tw,-H],[0.5*tw,-0.5*tf],[B,-0.5*tf]]
            sect_shape = [[0,-H],[0,0],[B,0]]
            sect_lin_con = [[3,2],[2,1]]
            sect_thk = [tw,tf]
            # sect_thk_off = [0,0]
            sect_thk_off = [tw/2,tf/2]
        
        elif shape.SHAPE == 'C' :
            H,B1,tw,tf1,B2,tf2 = shape.PARAMS[:6]
            if B2 == 0 : B2 = B1
            if tf2 == 0 : tf2 = tf1

            sect_cg_LT = [0,0]
            sect_cg_CC = [(B1+B2)*0.2,-H*0.5]
            sect_cg_RB = [max(B1,B2),-H]

            # sect_shape = [[0.5*tw,-0.5*tf1],[B1,-0.5*tf1],[0.5*tw,-H+0.5*tf2],[B2,-H+0.5*tf2]]
            sect_shape = [[0,0],[B1,0],[0,-H],[B2,-H]]
            sect_lin_con = [[2,1],[1,3],[3,4]]
            sect_thk = [tf1,tw,tf2]
            # sect_thk_off = [0,0,0]
            sect_thk_off = [tf1/2,tw/2,tf2/2]

        elif shape.SHAPE == 'H' :
            H,B1,tw,tf1,B2,tf2,r1,r2 = shape.PARAMS[:8]
            if B2 == 0 : B2 = B1
            if tf2 == 0 : tf2 = tf1

            sect_cg_LT = [-0.5*max(B1,B2),0.5*H]
            sect_cg_CC = [0,0]
            sect_cg_RB = [0.5*max(B1,B2),-0.5*H]

            sect_shape = [[-0.5*B1,0.5*(H-tf1)],[0,0.5*(H-tf1)],[0.5*B1,0.5*(H-tf1)],[-0.5*B2,-0.5*(H-tf2)],[0,-0.5*(H-tf2)],[0.5*B2,-0.5*(H-tf2)]]
            sect_lin_con = [[2,1],[3,2],[2,5],[4,5],[5,6]]
            sect_thk = [tf1,tf1,tw,tf2,tf2]
            sect_thk_off = [0,0,0,0,0]
        
        elif shape.SHAPE == 'T' :
            H,B,tw,tf = shape.PARAMS[:4]

            sect_cg_LT = [-B*0.5,0]
            sect_cg_CC = [0,-H*0.3]
            sect_cg_RB = [B*0.5,-H]

            sect_shape = [[-0.5*B,-0.5*tf],[0,-0.5*tf],[0.5*B,-0.5*tf],[0,-H]]
            sect_lin_con = [[2,1],[3,2],[2,4]]
            sect_thk = [tf,tf,tw]
            sect_thk_off = [0,0,0]

        elif shape.SHAPE == 'B' :
            H,B,tw,tf1,C,tf2 = shape.PARAMS[:6]
            if tf2 == 0 : tf2 = tf1

            sect_cg_LT = [-0.5*B,0.5*H]
            sect_cg_CC = [0,0]
            sect_cg_RB = [0.5*B,-0.5*H]

            # sect_shape = [[0.5*(B-tw),0.5*(H-tf1)],[-0.5*(B-tw),0.5*(H-tf1)],[-0.5*(B-tw),-0.5*(H-tf2)],[0.5*(B-tw),-0.5*(H-tf2)]]
            sect_shape = [[0.5*B,0.5*H],[-0.5*B,0.5*H],[-0.5*B,-0.5*H],[0.5*B,-0.5*H]]

            sect_lin_con = [[1,2],[2,3],[3,4],[4,1]]
            sect_thk = [tf1,tw,tf2,tw]
            # sect_thk_off = [0,0,0,0]
            sect_thk_off = [0.5*tf1,0.5*tw,0.5*tf2,0.5*tw]
        
        elif shape.SHAPE == 'P' :
            D,tw = shape.PARAMS[:2]

            # R = 0.5*(D-tw)
            R = 0.5*D

            sect_cg_LT = [-R,R]
            sect_cg_CC = [0,0]
            sect_cg_RB = [R,-R]

            sect_shape = []
            sect_lin_con = []
            sect_thk = []
            sect_thk_off = []

            n = 16
            for i in range(n):
                sect_shape.append([R*sin(i*2*pi/n),R*cos(i*2*pi/n)])
                sect_lin_con.append([i+1,i+2])
                sect_thk.append(tw)
                sect_thk_off.append(-0.5*tw)
            sect_lin_con[-1] = [i+1,1]



        sect_cg = (sect_cg_LT,sect_cg_CC,sect_cg_RB)

        return sect_shape, sect_thk ,sect_thk_off, sect_cg , sect_lin_con