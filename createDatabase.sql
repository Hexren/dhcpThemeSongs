--
-- Database: `dhcp_log`
--

-- --------------------------------------------------------

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
CREATE TABLE IF NOT EXISTS `events` (
  `action` enum('commit','release','expiry','remove') COLLATE utf8_unicode_ci NOT NULL,
  `tm` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `ip` varchar(15) COLLATE utf8_unicode_ci NOT NULL,
  `hw` varchar(30) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `state`
--

DROP TABLE IF EXISTS `state`;
CREATE TABLE IF NOT EXISTS `state` (
  `hw` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `state` enum('online','tentatively offline','offline') COLLATE utf8_unicode_ci NOT NULL,
  `lastIp` varchar(15) COLLATE utf8_unicode_ci NOT NULL,
  `lastSeen` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`hw`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

