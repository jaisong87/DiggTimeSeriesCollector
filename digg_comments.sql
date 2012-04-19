-- phpMyAdmin SQL Dump
-- version 3.3.9
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 16, 2012 at 04:00 AM
-- Server version: 5.5.8
-- PHP Version: 5.3.5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `digg_newdatabase`
--
USE DiggTimeSeriesCollector;
-- --------------------------------------------------------

--
-- Table structure for table `digg_comments`
--

CREATE TABLE IF NOT EXISTS `digg_comments` (
  `id` varchar(255) CHARACTER SET ascii NOT NULL,
  `story_id` varchar(255) CHARACTER SET ascii NOT NULL,
  `thread_id` varchar(255) CHARACTER SET ascii NOT NULL,
  `userid` varchar(255) CHARACTER SET ascii NOT NULL,
  `postdate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `comment_text` varchar(10000) NOT NULL,
  `diggs` int(11) NOT NULL,
  `diggsup` int(11) NOT NULL,
  `diggsdown` int(11) NOT NULL,
  `parent_id` varchar(255) CHARACTER SET ascii NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
