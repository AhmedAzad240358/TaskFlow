# TestLink Open Source Project - http://testlink.sourceforge.net/
# testlink_create_default_data.sql
# SQL script - create default data (rights & admin account)
#
# Database Type: MySQL
# ---------------------------------------------------------------------------------

# Database version
INSERT INTO db_version (version,notes,upgrade_ts) VALUES('DB 1.9.20', 'TestLink 1.9.20 Raijin',CURRENT_TIMESTAMP());

# Node types -
INSERT INTO node_types  (id,description) VALUES (1,'testproject');
INSERT INTO node_types  (id,description) VALUES (2,'testsuite');
INSERT INTO node_types  (id,description) VALUES (3,'testcase');
INSERT INTO node_types  (id,description) VALUES (4,'testcase_version');
INSERT INTO node_types  (id,description) VALUES (5,'testplan');
INSERT INTO node_types  (id,description) VALUES (6,'requirement_spec');
INSERT INTO node_types  (id,description) VALUES (7,'requirement');
INSERT INTO node_types  (id,description) VALUES (8,'requirement_version');
INSERT INTO node_types  (id,description) VALUES (9,'testcase_step');
INSERT INTO node_types  (id,description) VALUES (10,'requirement_revision');
INSERT INTO node_types  (id,description) VALUES (11,'requirement_spec_revision');
INSERT INTO node_types  (id,description) VALUES (12,'build');
INSERT INTO node_types  (id,description) VALUES (13,'platform');
INSERT INTO node_types  (id,description) VALUES (14,'user');


# Roles -
INSERT INTO roles  (id,description) VALUES (1, '<reserved system role 1>');
INSERT INTO roles  (id,description) VALUES (2, '<reserved system role 2>');
INSERT INTO roles  (id,description) VALUES (3, '<no rights>');
INSERT INTO roles  (id,description) VALUES (4, 'test designer');
INSERT INTO roles  (id,description) VALUES (5, 'guest');
INSERT INTO roles  (id,description) VALUES (6, 'senior tester');
INSERT INTO roles  (id,description) VALUES (7, 'tester');
INSERT INTO roles  (id,description) VALUES (8, 'admin');
INSERT INTO roles  (id,description) VALUES (9, 'leader');

# Rights - 
INSERT INTO rights  (id,description) VALUES (1 ,'testplan_execute');
INSERT INTO rights  (id,description) VALUES (2 ,'testplan_create_build');
INSERT INTO rights  (id,description) VALUES (3 ,'testplan_metrics');
INSERT INTO rights  (id,description) VALUES (4 ,'testplan_planning');
INSERT INTO rights  (id,description) VALUES (5 ,'testplan_user_role_assignment');
INSERT INTO rights  (id,description) VALUES (6 ,'mgt_view_tc');
INSERT INTO rights  (id,description) VALUES (7 ,'mgt_modify_tc');
INSERT INTO rights  (id,description) VALUES (8 ,'mgt_view_key');
INSERT INTO rights  (id,description) VALUES (9 ,'mgt_modify_key');
INSERT INTO rights  (id,description) VALUES (10,'mgt_view_req');
INSERT INTO rights  (id,description) VALUES (11,'mgt_modify_req');
INSERT INTO rights  (id,description) VALUES (12,'mgt_modify_product');
INSERT INTO rights  (id,description) VALUES (13,'mgt_users');
INSERT INTO rights  (id,description) VALUES (14,'role_management');
INSERT INTO rights  (id,description) VALUES (15,'user_role_assignment');
INSERT INTO rights  (id,description) VALUES (16,'mgt_testplan_create');
INSERT INTO rights  (id,description) VALUES (17,'cfield_view');
INSERT INTO rights  (id,description) VALUES (18,'cfield_management');
INSERT INTO rights  (id,description) VALUES (19,'system_configuration');
INSERT INTO rights  (id,description) VALUES (20,'mgt_view_events');
INSERT INTO rights  (id,description) VALUES (21,'mgt_view_usergroups');
INSERT INTO rights  (id,description) VALUES (22,'events_mgt');
INSERT INTO rights  (id,description) VALUES (23,'testproject_user_role_assignment');
INSERT INTO rights  (id,description) VALUES (24,'platform_management');
INSERT INTO rights  (id,description) VALUES (25,'platform_view');
INSERT INTO rights  (id,description) VALUES (26,'project_inventory_management');
INSERT INTO rights  (id,description) VALUES (27,'project_inventory_view');
INSERT INTO rights  (id,description) VALUES (28,'req_tcase_link_management');
INSERT INTO rights  (id,description) VALUES (29,'keyword_assignment');
INSERT INTO rights  (id,description) VALUES (30,'mgt_unfreeze_req');
INSERT INTO rights  (id,description) VALUES (31,'issuetracker_management');
INSERT INTO rights  (id,description) VALUES (32,'issuetracker_view');
INSERT INTO rights  (id,description) VALUES (33,'reqmgrsystem_management');
INSERT INTO rights  (id,description) VALUES (34,'reqmgrsystem_view');
INSERT INTO rights  (id,description) VALUES (35,'exec_edit_notes');
INSERT INTO rights  (id,description) VALUES (36,'exec_delete');
INSERT INTO rights  (id,description) VALUES (37,'testplan_unlink_executed_testcases');
INSERT INTO rights  (id,description) VALUES (38,'testproject_delete_executed_testcases');
INSERT INTO rights  (id,description) VALUES (39,'testproject_edit_executed_testcases');

# since 1.9.10
INSERT INTO rights  (id,description) VALUES (40,'testplan_milestone_overview');
INSERT INTO rights  (id,description) VALUES (41,'exec_testcases_assigned_to_me');
INSERT INTO rights  (id,description) VALUES (42,'testproject_metrics_dashboard');
INSERT INTO rights  (id,description) VALUES (43,'testplan_add_remove_platforms');
INSERT INTO rights  (id,description) VALUES (44,'testplan_update_linked_testcase_versions');
INSERT INTO rights  (id,description) VALUES (45,'testplan_set_urgent_testcases');
INSERT INTO rights  (id,description) VALUES (46,'testplan_show_testcases_newest_versions');
INSERT INTO rights  (id,description) VALUES (47,'testcase_freeze');

# since 1.9.15
INSERT INTO rights  (id,description) VALUES (48,'mgt_plugins');

-- since 1.9.17
INSERT INTO rights (id,description) VALUES (49,'exec_ro_access');
INSERT INTO rights (id,description) VALUES (50,'monitor_requirement');
INSERT INTO rights (id,description) VALUES (51,'codetracker_management');
INSERT INTO rights (id,description) VALUES (52,'codetracker_view');
INSERT INTO rights (id,description) VALUES (53,'cfield_assignment');
INSERT INTO rights (id,description) VALUES (54,'exec_assign_testcases');

-- since 1.9.20
INSERT INTO rights (id,description) VALUES (55,'testproject_add_remove_keywords_executed_tcversions');
INSERT INTO rights (id,description) VALUES (56,'delete_frozen_tcversion');

# Rights for Administrator role
INSERT INTO role_rights (role_id,right_id) VALUES (8,1 );
INSERT INTO role_rights (role_id,right_id) VALUES (8,2 );
INSERT INTO role_rights (role_id,right_id) VALUES (8,3 );
INSERT INTO role_rights (role_id,right_id) VALUES (8,4 );
INSERT INTO role_rights (role_id,right_id) VALUES (8,5 );
INSERT INTO role_rights (role_id,right_id) VALUES (8,6 );
INSERT INTO role_rights (role_id,right_id) VALUES (8,7 );
INSERT INTO role_rights (role_id,right_id) VALUES (8,8 );
INSERT INTO role_rights (role_id,right_id) VALUES (8,9 );
INSERT INTO role_rights (role_id,right_id) VALUES (8,10);
INSERT INTO role_rights (role_id,right_id) VALUES (8,11);
INSERT INTO role_rights (role_id,right_id) VALUES (8,12);
INSERT INTO role_rights (role_id,right_id) VALUES (8,13);
INSERT INTO role_rights (role_id,right_id) VALUES (8,14);
INSERT INTO role_rights (role_id,right_id) VALUES (8,15);
INSERT INTO role_rights (role_id,right_id) VALUES (8,16);
INSERT INTO role_rights (role_id,right_id) VALUES (8,17);
INSERT INTO role_rights (role_id,right_id) VALUES (8,18);
INSERT INTO role_rights (role_id,right_id) VALUES (8,19);
INSERT INTO role_rights (role_id,right_id) VALUES (8,20);
INSERT INTO role_rights (role_id,right_id) VALUES (8,21);
INSERT INTO role_rights (role_id,right_id) VALUES (8,22);
INSERT INTO role_rights (role_id,right_id) VALUES (8,23);
INSERT INTO role_rights (role_id,right_id) VALUES (8,24);
INSERT INTO role_rights (role_id,right_id) VALUES (8,25);
INSERT INTO role_rights (role_id,right_id) VALUES (8,26);
INSERT INTO role_rights (role_id,right_id) VALUES (8,27);
INSERT INTO role_rights (role_id,right_id) VALUES (8,28);
INSERT INTO role_rights (role_id,right_id) VALUES (8,29);
INSERT INTO role_rights (role_id,right_id) VALUES (8,30);
INSERT INTO role_rights (role_id,right_id) VALUES (8,31);
INSERT INTO role_rights (role_id,right_id) VALUES (8,32);
INSERT INTO role_rights (role_id,right_id) VALUES (8,33);
INSERT INTO role_rights (role_id,right_id) VALUES (8,34);
INSERT INTO role_rights (role_id,right_id) VALUES (8,35);
INSERT INTO role_rights (role_id,right_id) VALUES (8,36);
INSERT INTO role_rights (role_id,right_id) VALUES (8,37);
INSERT INTO role_rights (role_id,right_id) VALUES (8,38);
INSERT INTO role_rights (role_id,right_id) VALUES (8,39);
INSERT INTO role_rights (role_id,right_id) VALUES (8,40);
INSERT INTO role_rights (role_id,right_id) VALUES (8,41);
INSERT INTO role_rights (role_id,right_id) VALUES (8,42);
INSERT INTO role_rights (role_id,right_id) VALUES (8,43);
INSERT INTO role_rights (role_id,right_id) VALUES (8,44);
INSERT INTO role_rights (role_id,right_id) VALUES (8,45);
INSERT INTO role_rights (role_id,right_id) VALUES (8,46);
INSERT INTO role_rights (role_id,right_id) VALUES (8,47);
INSERT INTO role_rights (role_id,right_id) VALUES (8,48);
INSERT INTO role_rights (role_id,right_id) VALUES (8,50);
INSERT INTO role_rights (role_id,right_id) VALUES (8,51);
INSERT INTO role_rights (role_id,right_id) VALUES (8,52);
INSERT INTO role_rights (role_id,right_id) VALUES (8,53);
INSERT INTO role_rights (role_id,right_id) VALUES (8,54);

# Rights for guest role
INSERT INTO role_rights (role_id,right_id) VALUES (5,3 );
INSERT INTO role_rights (role_id,right_id) VALUES (5,6 );
INSERT INTO role_rights (role_id,right_id) VALUES (5,8 );

# Rights for test designer role
INSERT INTO role_rights (role_id,right_id) VALUES (4,3 );
INSERT INTO role_rights (role_id,right_id) VALUES (4,6 );
INSERT INTO role_rights (role_id,right_id) VALUES (4,7 );
INSERT INTO role_rights (role_id,right_id) VALUES (4,8 );
INSERT INTO role_rights (role_id,right_id) VALUES (4,9 );
INSERT INTO role_rights (role_id,right_id) VALUES (4,10);
INSERT INTO role_rights (role_id,right_id) VALUES (4,11);
INSERT INTO role_rights (role_id,right_id) VALUES (4,28);
INSERT INTO role_rights (role_id,right_id) VALUES (4,29);
INSERT INTO role_rights (role_id,right_id) VALUES (4,30);
INSERT INTO role_rights (role_id,right_id) VALUES (4,50);

# Rights for tester role
INSERT INTO role_rights (role_id,right_id) VALUES (7,1 );
INSERT INTO role_rights (role_id,right_id) VALUES (7,3 );
INSERT INTO role_rights (role_id,right_id) VALUES (7,6 );
INSERT INTO role_rights (role_id,right_id) VALUES (7,8 );

# Rights for senior tester role
INSERT INTO role_rights (role_id,right_id) VALUES (6,1 );
INSERT INTO role_rights (role_id,right_id) VALUES (6,2 );
INSERT INTO role_rights (role_id,right_id) VALUES (6,3 );
INSERT INTO role_rights (role_id,right_id) VALUES (6,6 );
INSERT INTO role_rights (role_id,right_id) VALUES (6,7 );
INSERT INTO role_rights (role_id,right_id) VALUES (6,8 );
INSERT INTO role_rights (role_id,right_id) VALUES (6,9 );
INSERT INTO role_rights (role_id,right_id) VALUES (6,11);
INSERT INTO role_rights (role_id,right_id) VALUES (6,25);
INSERT INTO role_rights (role_id,right_id) VALUES (6,27);
INSERT INTO role_rights (role_id,right_id) VALUES (6,28);
INSERT INTO role_rights (role_id,right_id) VALUES (6,29);
INSERT INTO role_rights (role_id,right_id) VALUES (6,30);
INSERT INTO role_rights (role_id,right_id) VALUES (6,50);

# Rights for leader role
INSERT INTO role_rights (role_id,right_id) VALUES (9,1 );
INSERT INTO role_rights (role_id,right_id) VALUES (9,2 );
INSERT INTO role_rights (role_id,right_id) VALUES (9,3 );
INSERT INTO role_rights (role_id,right_id) VALUES (9,4 );
INSERT INTO role_rights (role_id,right_id) VALUES (9,5 );
INSERT INTO role_rights (role_id,right_id) VALUES (9,6 );
INSERT INTO role_rights (role_id,right_id) VALUES (9,7 );
INSERT INTO role_rights (role_id,right_id) VALUES (9,8 );
INSERT INTO role_rights (role_id,right_id) VALUES (9,9 );
INSERT INTO role_rights (role_id,right_id) VALUES (9,10);
INSERT INTO role_rights (role_id,right_id) VALUES (9,11);
INSERT INTO role_rights (role_id,right_id) VALUES (9,15);
INSERT INTO role_rights (role_id,right_id) VALUES (9,16);
INSERT INTO role_rights (role_id,right_id) VALUES (9,24);
INSERT INTO role_rights (role_id,right_id) VALUES (9,25);
INSERT INTO role_rights (role_id,right_id) VALUES (9,26);
INSERT INTO role_rights (role_id,right_id) VALUES (9,27);
INSERT INTO role_rights (role_id,right_id) VALUES (9,28);
INSERT INTO role_rights (role_id,right_id) VALUES (9,29);
INSERT INTO role_rights (role_id,right_id) VALUES (9,30);
INSERT INTO role_rights (role_id,right_id) VALUES (9,47);
INSERT INTO role_rights (role_id,right_id) VALUES (9,50);

# admin account 
# SECURITY: change password after first login
#
# TICKET 4342: Security problem with multiple Testlink installations on the same server 
INSERT INTO users (login,password,role_id,email,first,last,locale,active,cookie_string)
			VALUES ('admin',MD5('admin'), 8,'', 'Testlink','Administrator', 'en_GB',1,CONCAT(MD5(RAND()),MD5('admin')));


# Assignment types
INSERT INTO assignment_types (id,fk_table,description) VALUES(1,'testplan_tcversions','testcase_execution');
INSERT INTO assignment_types (id,fk_table,description) VALUES(2,'tcversions','testcase_review');

# Assignment status
INSERT INTO assignment_status (id,description) VALUES(1,'open');
INSERT INTO assignment_status (id,description) VALUES(2,'closed');
INSERT INTO assignment_status (id,description) VALUES(3,'completed');
INSERT INTO assignment_status (id,description) VALUES(4,'todo_urgent');
INSERT INTO assignment_status (id,description) VALUES(5,'todo');
