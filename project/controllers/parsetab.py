
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND AUTO_INCREMENT BIGINT BOOLEAN COMMA COMPARISON CREATE DATABASE DATE DATETIME DECIMAL DELETE DIVIDE DOUBLE DOUBLEQUOTE DROP EQUALS FLOAT FROM FULL GREATERTHAN ID INDEX INNER INSERT INT INTEGER INTO JOIN LEFT LESSTHAN LONGTEXT LPAREN MEDIUMINT MEDIUMTEXT MINUS NOT NOTNULL NULL NUMBER NUMERIC ON OR OUTER PLUS POINT PRIMARY PRIMARYKEY REAL RIGHT RPAREN SELECT SEMICOLON SERIAL SET SIMPLEQUOTE SMALLINT STRING TABLE TEXT TIME TIMES TINYINT TINYTEXT UPDATE VALUES VARCHAR WHERE\n    statement : select_statement\n              | create_statement\n              | insert_statement\n              | update_statement\n              | delete_statement\n              | drop_statement\n    \n    select_statement : SELECT column_list FROM table_reference SEMICOLON\n                    | SELECT column_list FROM table_reference join_clause SEMICOLON\n                    | SELECT column_list FROM table_reference where_clause SEMICOLON\n                    | SELECT column_list FROM table_reference join_clause where_clause SEMICOLON\n    \n    where_clause : WHERE condition\n    \n    join_clause : join_clause join_type JOIN table_reference ON condition\n                | join_type JOIN table_reference ON condition\n    \n    join_type : INNER\n              | LEFT\n              | RIGHT\n              | FULL\n              | LEFT OUTER\n              | RIGHT OUTER\n              | FULL OUTER\n    \n    column_list : column\n                | column_list COMMA column\n    \n    column : ID\n           | ID POINT ID\n    \n    table_reference : ID\n    \n    condition : expression AND expression\n              | expression OR expression\n              | NOT condition\n              | expression EQUALS expression\n              | expression EQUALS string\n              | expression LESSTHAN expression\n              | expression GREATERTHAN expression\n              | expression COMPARISON expression\n              | column COMPARISON expression\n              | LPAREN condition RPAREN\n              | ID EQUALS NUMBER\n              | ID EQUALS ID\n              | STRING EQUALS STRING\n              | column COMPARISON ID\n              | column EQUALS ID\n              | column EQUALS column\n    \n    insert_statement : INSERT INTO ID LPAREN column_list RPAREN VALUES LPAREN value_list RPAREN SEMICOLON\n    \n    value_list : value\n               | value_list COMMA value\n    \n    value : NUMBER\n          | string\n    \n    update_statement : UPDATE ID SET set_clause where_clause SEMICOLON\n                        | UPDATE ID SET set_clause  SEMICOLON\n    \n    set_clause : assignment\n               | set_clause COMMA assignment\n    \n    assignment : ID EQUALS value\n    \n    delete_statement : DELETE FROM ID where_clause SEMICOLON\n    \n    drop_statement : DROP DATABASE ID SEMICOLON\n                   | DROP TABLE ID SEMICOLON\n                   | DROP INDEX ID SEMICOLON\n    \n    create_statement : create_database_statement\n                     | create_table_statement\n                     | create_index_statement\n    \n    create_database_statement : CREATE DATABASE ID SEMICOLON\n    \n    create_table_statement : CREATE TABLE ID LPAREN column_definitions RPAREN SEMICOLON\n    \n    column_definitions : column_definition\n                       | column_definitions COMMA column_definition\n    \n    column_definition : ID data_type column_constraint_list\n    \n    column_constraint_list : column_constraint\n                           | column_constraint_list column_constraint\n    \n    column_constraint : NOTNULL\n                     | NULL\n                     | AUTO_INCREMENT PRIMARYKEY\n                     | PRIMARYKEY\n                     | empty\n    empty :\n    data_type : INT\n              | VARCHAR LPAREN NUMBER RPAREN\n              | DATE\n              | FLOAT\n              | TEXT\n              | BOOLEAN\n              | TINYINT\n              | SMALLINT\n              | MEDIUMINT\n              | INTEGER\n              | BIGINT\n              | REAL\n              | DOUBLE\n              | DECIMAL\n              | NUMERIC\n              | TIME\n              | DATETIME\n              | TINYTEXT\n              | MEDIUMTEXT\n              | LONGTEXT\n              | TIMES\n              | MINUS\n              | SERIAL\n    \n    create_index_statement : CREATE INDEX ID ON ID LPAREN ID RPAREN SEMICOLON\n    \n    expression : expression PLUS expression\n               | expression MINUS expression\n               | expression TIMES expression\n               | expression DIVIDE expression\n               | LPAREN expression RPAREN\n               | NUMBER\n               | ID\n    \n    string : DOUBLEQUOTE ID DOUBLEQUOTE\n           | SIMPLEQUOTE ID SIMPLEQUOTE\n    '
    
_lr_action_items = {'SELECT':([0,],[8,]),'INSERT':([0,],[12,]),'UPDATE':([0,],[13,]),'DELETE':([0,],[14,]),'DROP':([0,],[15,]),'CREATE':([0,],[16,]),'$end':([1,2,3,4,5,6,7,9,10,11,51,52,53,54,57,68,70,83,86,97,143,179,197,201,],[0,-1,-2,-3,-4,-5,-6,-56,-57,-58,-53,-54,-55,-59,-7,-48,-52,-8,-9,-47,-10,-60,-95,-42,]),'ID':([8,13,20,22,23,24,25,26,27,28,29,30,31,33,45,50,55,56,69,73,75,87,95,96,99,100,101,102,103,104,105,106,107,108,110,111,114,141,142,144,150,183,192,],[19,21,32,34,35,36,37,38,39,40,42,19,44,46,19,76,79,82,46,76,76,42,147,148,151,151,151,151,151,151,151,151,151,151,163,165,168,79,181,42,151,76,76,]),'INTO':([12,],[20,]),'FROM':([14,17,18,19,43,44,],[22,29,-21,-23,-22,-24,]),'DATABASE':([15,16,],[23,26,]),'TABLE':([15,16,],[24,27,]),'INDEX':([15,16,],[25,28,]),'COMMA':([17,18,19,43,44,47,48,65,80,81,92,93,94,98,116,117,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,171,172,173,174,176,177,180,185,186,188,189,194,195,196,202,],[30,-21,-23,-22,-24,69,-49,30,141,-61,-51,-45,-46,-50,-71,-72,-74,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,-63,-64,-66,-67,-69,-70,-62,-103,-104,-65,-68,200,-43,-73,-44,]),'RPAREN':([18,19,43,44,65,76,77,80,81,93,94,109,112,113,116,117,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,149,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,176,177,180,181,185,186,187,188,189,190,194,195,196,202,],[-21,-23,-22,-24,91,-102,-101,140,-61,-45,-46,-28,166,167,-71,-72,-74,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,-26,-102,-27,-29,-30,-31,-32,-33,-96,-97,-98,-99,-34,-39,-41,-23,-35,-100,-37,-36,-38,-63,-64,-66,-67,-69,-70,-62,191,-103,-104,167,-65,-68,196,199,-43,-73,-44,]),'POINT':([19,76,165,],[31,31,31,]),'SET':([21,],[33,]),'LPAREN':([32,39,50,73,75,82,99,100,101,102,103,104,105,106,107,108,110,118,146,150,183,192,],[45,55,75,75,75,142,150,150,150,150,150,150,150,150,150,150,150,178,184,150,75,75,]),'WHERE':([34,41,42,44,47,48,58,77,92,93,94,98,109,149,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,185,186,193,198,],[50,50,-25,-24,50,-49,50,-101,-51,-45,-46,-50,-28,-26,-102,-27,-29,-30,-31,-32,-33,-96,-97,-98,-99,-34,-39,-41,-23,-35,-100,-37,-36,-38,-103,-104,-13,-12,]),'SEMICOLON':([35,36,37,38,41,42,44,47,48,49,58,59,67,71,77,84,92,93,94,98,109,140,149,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,185,186,191,193,198,199,],[51,52,53,54,57,-25,-24,68,-49,70,83,86,97,-11,-101,143,-51,-45,-46,-50,-28,179,-26,-102,-27,-29,-30,-31,-32,-33,-96,-97,-98,-99,-34,-39,-41,-23,-35,-100,-37,-36,-38,-103,-104,197,-13,-12,201,]),'ON':([40,42,145,182,],[56,-25,183,192,]),'INNER':([41,42,44,58,77,109,149,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,185,186,193,198,],[61,-25,-24,61,-101,-28,-26,-102,-27,-29,-30,-31,-32,-33,-96,-97,-98,-99,-34,-39,-41,-23,-35,-100,-37,-36,-38,-103,-104,-13,-12,]),'LEFT':([41,42,44,58,77,109,149,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,185,186,193,198,],[62,-25,-24,62,-101,-28,-26,-102,-27,-29,-30,-31,-32,-33,-96,-97,-98,-99,-34,-39,-41,-23,-35,-100,-37,-36,-38,-103,-104,-13,-12,]),'RIGHT':([41,42,44,58,77,109,149,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,185,186,193,198,],[63,-25,-24,63,-101,-28,-26,-102,-27,-29,-30,-31,-32,-33,-96,-97,-98,-99,-34,-39,-41,-23,-35,-100,-37,-36,-38,-103,-104,-13,-12,]),'FULL':([41,42,44,58,77,109,149,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,185,186,193,198,],[64,-25,-24,64,-101,-28,-26,-102,-27,-29,-30,-31,-32,-33,-96,-97,-98,-99,-34,-39,-41,-23,-35,-100,-37,-36,-38,-103,-104,-13,-12,]),'COMPARISON':([44,72,74,76,77,113,151,158,159,160,161,167,],[-24,104,110,-23,-101,104,-102,-96,-97,-98,-99,-100,]),'EQUALS':([44,46,72,74,76,77,78,113,151,158,159,160,161,167,],[-24,66,101,111,114,-101,115,101,-102,-96,-97,-98,-99,-100,]),'NOT':([50,73,75,183,192,],[73,73,73,73,73,]),'STRING':([50,73,75,115,183,192,],[78,78,78,170,78,78,]),'NUMBER':([50,66,73,75,99,100,101,102,103,104,105,106,107,108,110,114,150,178,183,184,192,200,],[77,93,77,77,77,77,77,77,77,77,77,77,77,77,77,169,77,190,77,93,77,93,]),'JOIN':([60,61,62,63,64,85,88,89,90,],[87,-14,-15,-16,-17,144,-18,-19,-20,]),'OUTER':([62,63,64,],[88,89,90,]),'DOUBLEQUOTE':([66,101,147,184,200,],[95,95,185,95,95,]),'SIMPLEQUOTE':([66,101,148,184,200,],[96,96,186,96,96,]),'AND':([72,76,77,113,151,158,159,160,161,167,],[99,-102,-101,99,-102,-96,-97,-98,-99,-100,]),'OR':([72,76,77,113,151,158,159,160,161,167,],[100,-102,-101,100,-102,-96,-97,-98,-99,-100,]),'LESSTHAN':([72,76,77,113,151,158,159,160,161,167,],[102,-102,-101,102,-102,-96,-97,-98,-99,-100,]),'GREATERTHAN':([72,76,77,113,151,158,159,160,161,167,],[103,-102,-101,103,-102,-96,-97,-98,-99,-100,]),'PLUS':([72,76,77,113,149,151,152,153,155,156,157,158,159,160,161,162,163,167,187,],[105,-102,-101,105,105,-102,105,105,105,105,105,105,105,105,105,105,-102,-100,105,]),'MINUS':([72,76,77,79,113,149,151,152,153,155,156,157,158,159,160,161,162,163,167,187,],[106,-102,-101,138,106,106,-102,106,106,106,106,106,106,106,106,106,106,-102,-100,106,]),'TIMES':([72,76,77,79,113,149,151,152,153,155,156,157,158,159,160,161,162,163,167,187,],[107,-102,-101,137,107,107,-102,107,107,107,107,107,107,107,107,107,107,-102,-100,107,]),'DIVIDE':([72,76,77,113,149,151,152,153,155,156,157,158,159,160,161,162,163,167,187,],[108,-102,-101,108,108,-102,108,108,108,108,108,108,108,108,108,108,-102,-100,108,]),'INT':([79,],[117,]),'VARCHAR':([79,],[118,]),'DATE':([79,],[119,]),'FLOAT':([79,],[120,]),'TEXT':([79,],[121,]),'BOOLEAN':([79,],[122,]),'TINYINT':([79,],[123,]),'SMALLINT':([79,],[124,]),'MEDIUMINT':([79,],[125,]),'INTEGER':([79,],[126,]),'BIGINT':([79,],[127,]),'REAL':([79,],[128,]),'DOUBLE':([79,],[129,]),'DECIMAL':([79,],[130,]),'NUMERIC':([79,],[131,]),'TIME':([79,],[132,]),'DATETIME':([79,],[133,]),'TINYTEXT':([79,],[134,]),'MEDIUMTEXT':([79,],[135,]),'LONGTEXT':([79,],[136,]),'SERIAL':([79,],[139,]),'VALUES':([91,],[146,]),'NOTNULL':([116,117,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,171,172,173,174,176,177,188,189,196,],[173,-72,-74,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,173,-64,-66,-67,-69,-70,-65,-68,-73,]),'NULL':([116,117,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,171,172,173,174,176,177,188,189,196,],[174,-72,-74,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,174,-64,-66,-67,-69,-70,-65,-68,-73,]),'AUTO_INCREMENT':([116,117,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,171,172,173,174,176,177,188,189,196,],[175,-72,-74,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,175,-64,-66,-67,-69,-70,-65,-68,-73,]),'PRIMARYKEY':([116,117,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,171,172,173,174,175,176,177,188,189,196,],[176,-72,-74,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,176,-64,-66,-67,189,-69,-70,-65,-68,-73,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statement':([0,],[1,]),'select_statement':([0,],[2,]),'create_statement':([0,],[3,]),'insert_statement':([0,],[4,]),'update_statement':([0,],[5,]),'delete_statement':([0,],[6,]),'drop_statement':([0,],[7,]),'create_database_statement':([0,],[9,]),'create_table_statement':([0,],[10,]),'create_index_statement':([0,],[11,]),'column_list':([8,45,],[17,65,]),'column':([8,30,45,50,73,75,111,183,192,],[18,43,18,74,74,74,164,74,74,]),'table_reference':([29,87,144,],[41,145,182,]),'set_clause':([33,],[47,]),'assignment':([33,69,],[48,98,]),'where_clause':([34,41,47,58,],[49,59,67,84,]),'join_clause':([41,],[58,]),'join_type':([41,58,],[60,85,]),'condition':([50,73,75,183,192,],[71,109,112,193,198,]),'expression':([50,73,75,99,100,101,102,103,104,105,106,107,108,110,150,183,192,],[72,72,113,149,152,153,155,156,157,158,159,160,161,162,187,72,72,]),'column_definitions':([55,],[80,]),'column_definition':([55,141,],[81,180,]),'value':([66,184,200,],[92,195,202,]),'string':([66,101,184,200,],[94,154,94,94,]),'data_type':([79,],[116,]),'column_constraint_list':([116,],[171,]),'column_constraint':([116,171,],[172,188,]),'empty':([116,171,],[177,177,]),'value_list':([184,],[194,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> select_statement','statement',1,'p_statement','parser.py',10),
  ('statement -> create_statement','statement',1,'p_statement','parser.py',11),
  ('statement -> insert_statement','statement',1,'p_statement','parser.py',12),
  ('statement -> update_statement','statement',1,'p_statement','parser.py',13),
  ('statement -> delete_statement','statement',1,'p_statement','parser.py',14),
  ('statement -> drop_statement','statement',1,'p_statement','parser.py',15),
  ('select_statement -> SELECT column_list FROM table_reference SEMICOLON','select_statement',5,'p_select_statement','parser.py',22),
  ('select_statement -> SELECT column_list FROM table_reference join_clause SEMICOLON','select_statement',6,'p_select_statement','parser.py',23),
  ('select_statement -> SELECT column_list FROM table_reference where_clause SEMICOLON','select_statement',6,'p_select_statement','parser.py',24),
  ('select_statement -> SELECT column_list FROM table_reference join_clause where_clause SEMICOLON','select_statement',7,'p_select_statement','parser.py',25),
  ('where_clause -> WHERE condition','where_clause',2,'p_where_clause','parser.py',37),
  ('join_clause -> join_clause join_type JOIN table_reference ON condition','join_clause',6,'p_join_clause','parser.py',47),
  ('join_clause -> join_type JOIN table_reference ON condition','join_clause',5,'p_join_clause','parser.py',48),
  ('join_type -> INNER','join_type',1,'p_join_type','parser.py',57),
  ('join_type -> LEFT','join_type',1,'p_join_type','parser.py',58),
  ('join_type -> RIGHT','join_type',1,'p_join_type','parser.py',59),
  ('join_type -> FULL','join_type',1,'p_join_type','parser.py',60),
  ('join_type -> LEFT OUTER','join_type',2,'p_join_type','parser.py',61),
  ('join_type -> RIGHT OUTER','join_type',2,'p_join_type','parser.py',62),
  ('join_type -> FULL OUTER','join_type',2,'p_join_type','parser.py',63),
  ('column_list -> column','column_list',1,'p_column_list','parser.py',72),
  ('column_list -> column_list COMMA column','column_list',3,'p_column_list','parser.py',73),
  ('column -> ID','column',1,'p_column','parser.py',82),
  ('column -> ID POINT ID','column',3,'p_column','parser.py',83),
  ('table_reference -> ID','table_reference',1,'p_table_reference','parser.py',93),
  ('condition -> expression AND expression','condition',3,'p_condition','parser.py',99),
  ('condition -> expression OR expression','condition',3,'p_condition','parser.py',100),
  ('condition -> NOT condition','condition',2,'p_condition','parser.py',101),
  ('condition -> expression EQUALS expression','condition',3,'p_condition','parser.py',102),
  ('condition -> expression EQUALS string','condition',3,'p_condition','parser.py',103),
  ('condition -> expression LESSTHAN expression','condition',3,'p_condition','parser.py',104),
  ('condition -> expression GREATERTHAN expression','condition',3,'p_condition','parser.py',105),
  ('condition -> expression COMPARISON expression','condition',3,'p_condition','parser.py',106),
  ('condition -> column COMPARISON expression','condition',3,'p_condition','parser.py',107),
  ('condition -> LPAREN condition RPAREN','condition',3,'p_condition','parser.py',108),
  ('condition -> ID EQUALS NUMBER','condition',3,'p_condition','parser.py',109),
  ('condition -> ID EQUALS ID','condition',3,'p_condition','parser.py',110),
  ('condition -> STRING EQUALS STRING','condition',3,'p_condition','parser.py',111),
  ('condition -> column COMPARISON ID','condition',3,'p_condition','parser.py',112),
  ('condition -> column EQUALS ID','condition',3,'p_condition','parser.py',113),
  ('condition -> column EQUALS column','condition',3,'p_condition','parser.py',114),
  ('insert_statement -> INSERT INTO ID LPAREN column_list RPAREN VALUES LPAREN value_list RPAREN SEMICOLON','insert_statement',11,'p_insert_statement','parser.py',138),
  ('value_list -> value','value_list',1,'p_value_list','parser.py',144),
  ('value_list -> value_list COMMA value','value_list',3,'p_value_list','parser.py',145),
  ('value -> NUMBER','value',1,'p_value','parser.py',154),
  ('value -> string','value',1,'p_value','parser.py',155),
  ('update_statement -> UPDATE ID SET set_clause where_clause SEMICOLON','update_statement',6,'p_update_statement','parser.py',161),
  ('update_statement -> UPDATE ID SET set_clause SEMICOLON','update_statement',5,'p_update_statement','parser.py',162),
  ('set_clause -> assignment','set_clause',1,'p_set_clause','parser.py',168),
  ('set_clause -> set_clause COMMA assignment','set_clause',3,'p_set_clause','parser.py',169),
  ('assignment -> ID EQUALS value','assignment',3,'p_assignment','parser.py',178),
  ('delete_statement -> DELETE FROM ID where_clause SEMICOLON','delete_statement',5,'p_delete_statement','parser.py',184),
  ('drop_statement -> DROP DATABASE ID SEMICOLON','drop_statement',4,'p_drop_statement','parser.py',190),
  ('drop_statement -> DROP TABLE ID SEMICOLON','drop_statement',4,'p_drop_statement','parser.py',191),
  ('drop_statement -> DROP INDEX ID SEMICOLON','drop_statement',4,'p_drop_statement','parser.py',192),
  ('create_statement -> create_database_statement','create_statement',1,'p_create_statement','parser.py',198),
  ('create_statement -> create_table_statement','create_statement',1,'p_create_statement','parser.py',199),
  ('create_statement -> create_index_statement','create_statement',1,'p_create_statement','parser.py',200),
  ('create_database_statement -> CREATE DATABASE ID SEMICOLON','create_database_statement',4,'p_create_database_statement','parser.py',206),
  ('create_table_statement -> CREATE TABLE ID LPAREN column_definitions RPAREN SEMICOLON','create_table_statement',7,'p_create_table_statement','parser.py',212),
  ('column_definitions -> column_definition','column_definitions',1,'p_column_definitions','parser.py',218),
  ('column_definitions -> column_definitions COMMA column_definition','column_definitions',3,'p_column_definitions','parser.py',219),
  ('column_definition -> ID data_type column_constraint_list','column_definition',3,'p_column_definition','parser.py',228),
  ('column_constraint_list -> column_constraint','column_constraint_list',1,'p_column_constraint_list','parser.py',234),
  ('column_constraint_list -> column_constraint_list column_constraint','column_constraint_list',2,'p_column_constraint_list','parser.py',235),
  ('column_constraint -> NOTNULL','column_constraint',1,'p_column_constraint','parser.py',244),
  ('column_constraint -> NULL','column_constraint',1,'p_column_constraint','parser.py',245),
  ('column_constraint -> AUTO_INCREMENT PRIMARYKEY','column_constraint',2,'p_column_constraint','parser.py',246),
  ('column_constraint -> PRIMARYKEY','column_constraint',1,'p_column_constraint','parser.py',247),
  ('column_constraint -> empty','column_constraint',1,'p_column_constraint','parser.py',248),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',257),
  ('data_type -> INT','data_type',1,'p_data_type','parser.py',263),
  ('data_type -> VARCHAR LPAREN NUMBER RPAREN','data_type',4,'p_data_type','parser.py',264),
  ('data_type -> DATE','data_type',1,'p_data_type','parser.py',265),
  ('data_type -> FLOAT','data_type',1,'p_data_type','parser.py',266),
  ('data_type -> TEXT','data_type',1,'p_data_type','parser.py',267),
  ('data_type -> BOOLEAN','data_type',1,'p_data_type','parser.py',268),
  ('data_type -> TINYINT','data_type',1,'p_data_type','parser.py',269),
  ('data_type -> SMALLINT','data_type',1,'p_data_type','parser.py',270),
  ('data_type -> MEDIUMINT','data_type',1,'p_data_type','parser.py',271),
  ('data_type -> INTEGER','data_type',1,'p_data_type','parser.py',272),
  ('data_type -> BIGINT','data_type',1,'p_data_type','parser.py',273),
  ('data_type -> REAL','data_type',1,'p_data_type','parser.py',274),
  ('data_type -> DOUBLE','data_type',1,'p_data_type','parser.py',275),
  ('data_type -> DECIMAL','data_type',1,'p_data_type','parser.py',276),
  ('data_type -> NUMERIC','data_type',1,'p_data_type','parser.py',277),
  ('data_type -> TIME','data_type',1,'p_data_type','parser.py',278),
  ('data_type -> DATETIME','data_type',1,'p_data_type','parser.py',279),
  ('data_type -> TINYTEXT','data_type',1,'p_data_type','parser.py',280),
  ('data_type -> MEDIUMTEXT','data_type',1,'p_data_type','parser.py',281),
  ('data_type -> LONGTEXT','data_type',1,'p_data_type','parser.py',282),
  ('data_type -> TIMES','data_type',1,'p_data_type','parser.py',283),
  ('data_type -> MINUS','data_type',1,'p_data_type','parser.py',284),
  ('data_type -> SERIAL','data_type',1,'p_data_type','parser.py',285),
  ('create_index_statement -> CREATE INDEX ID ON ID LPAREN ID RPAREN SEMICOLON','create_index_statement',9,'p_create_index_statement','parser.py',291),
  ('expression -> expression PLUS expression','expression',3,'p_expression','parser.py',297),
  ('expression -> expression MINUS expression','expression',3,'p_expression','parser.py',298),
  ('expression -> expression TIMES expression','expression',3,'p_expression','parser.py',299),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression','parser.py',300),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression','parser.py',301),
  ('expression -> NUMBER','expression',1,'p_expression','parser.py',302),
  ('expression -> ID','expression',1,'p_expression','parser.py',303),
  ('string -> DOUBLEQUOTE ID DOUBLEQUOTE','string',3,'p_string','parser.py',320),
  ('string -> SIMPLEQUOTE ID SIMPLEQUOTE','string',3,'p_string','parser.py',321),
]