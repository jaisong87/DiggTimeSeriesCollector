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

-- --------------------------------------------------------

--
-- Table structure for table `diggs_diggs`
--

CREATE TABLE IF NOT EXISTS `diggs_diggs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `digg_id` varchar(250) NOT NULL,
  `digg_created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `time_queried` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `diggs` int(11) NOT NULL,
  `comments` int(11) NOT NULL,
  `diggsup` int(11) NOT NULL,
  `diggsdown` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=508 ;
