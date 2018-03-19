/*
Navicat MySQL Data Transfer

Source Server         : 00_开发环境_23006
Source Server Version : 50628
Source Host           : 172.16.81.62:23006
Source Database       : datahouse

Target Server Type    : MYSQL
Target Server Version : 50628
File Encoding         : 65001

Date: 2018-03-19 14:40:27
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for instance
-- ----------------------------
DROP TABLE IF EXISTS `instance`;
CREATE TABLE `instance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `host` varchar(50) NOT NULL DEFAULT '',
  `port` varchar(50) NOT NULL DEFAULT '',
  `db_usage` varchar(50) NOT NULL DEFAULT '',
  `db_type` varchar(50) NOT NULL,
  `project_id` int(11) DEFAULT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_instance_create_time` (`create_time`) USING BTREE,
  KEY `instance.project_id_project.id` (`project_id`) USING BTREE,
  CONSTRAINT `instance_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for project
-- ----------------------------
DROP TABLE IF EXISTS `project`;
CREATE TABLE `project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL DEFAULT '',
  `type` varchar(50) NOT NULL DEFAULT '',
  `pro_uid` varchar(50) DEFAULT NULL,
  `pm` varchar(50) DEFAULT NULL,
  `op` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for size
-- ----------------------------
DROP TABLE IF EXISTS `size`;
CREATE TABLE `size` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `size` varchar(500) NOT NULL DEFAULT '',
  `tactics` varchar(8) NOT NULL,
  `time_cost` varchar(8) NOT NULL,
  `instance_id` int(11) DEFAULT NULL,
  `agent_date` date NOT NULL,
  `agent_datetime` datetime DEFAULT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_info_info_id` (`instance_id`) USING BTREE,
  CONSTRAINT `size_ibfk_1` FOREIGN KEY (`instance_id`) REFERENCES `instance` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4912 DEFAULT CHARSET=utf8;
