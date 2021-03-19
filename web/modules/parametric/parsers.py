from flask_restx import reqparse

parametric_parser = reqparse.RequestParser()
parametric_parser.add_argument('oid',
                               type=str,
                               required=True,
                               help='ZTF Object ID')
parametric_parser.add_argument('days',
                               type=int,
                               default = 0,
                               help='Number of days to next forecast')
