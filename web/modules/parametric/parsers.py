from flask_restx import reqparse

parametric_parser = reqparse.RequestParser()
parametric_parser.add_argument('oid',
                               type=str,
                               required=True,
                               help='ZTF Object ID')
parametric_parser.add_argument('mjd',
                               type=float,
                               action='append',
                               help='Modified julian date to next forecast')
