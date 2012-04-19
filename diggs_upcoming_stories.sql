-- phpMyAdmin SQL Dump
-- version 3.3.9
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 16, 2012 at 03:59 AM
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

-- --------------------------------------------------------

--
-- Table structure for table `diggs_upcoming_stories`
--

CREATE TABLE IF NOT EXISTS `diggs_upcoming_stories` (
  `digg_id` varchar(200) CHARACTER SET ascii NOT NULL,
  `url` varchar(250) CHARACTER SET ascii NOT NULL,
  `diggurl` varchar(255) CHARACTER SET ascii NOT NULL,
  `categoryname` varchar(100) CHARACTER SET ascii NOT NULL,
  `userid` varchar(100) CHARACTER SET ascii NOT NULL,
  `postdate` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `title` varchar(255) CHARACTER SET ascii NOT NULL,
  `description` longtext CHARACTER SET ascii NOT NULL,
  `diggs` int(11) NOT NULL,
  `noofcomments` int(11) NOT NULL,
  `status` varchar(100) NOT NULL,
  PRIMARY KEY (`digg_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
