-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : lun. 03 juin 2024 à 20:11
-- Version du serveur : 8.0.31
-- Version de PHP : 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `moto`
--

-- --------------------------------------------------------

--
-- Structure de la table `lieux_de_vente`
--

DROP TABLE IF EXISTS `lieux_de_vente`;
CREATE TABLE IF NOT EXISTS `lieux_de_vente` (
  `idLieux` int NOT NULL AUTO_INCREMENT,
  `nomMagasin` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT 'particulier',
  `adresse` varchar(70) NOT NULL,
  `codePostal` int NOT NULL,
  `ville` varchar(50) NOT NULL,
  PRIMARY KEY (`idLieux`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Structure de la table `marque`
--

DROP TABLE IF EXISTS `marque`;
CREATE TABLE IF NOT EXISTS `marque` (
  `idMarque` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(20) NOT NULL,
  `nationnalité` varchar(50) NOT NULL,
  PRIMARY KEY (`idMarque`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Structure de la table `moto`
--

DROP TABLE IF EXISTS `moto`;
CREATE TABLE IF NOT EXISTS `moto` (
  `idMoto` int NOT NULL AUTO_INCREMENT,
  `modèle` varchar(20) NOT NULL,
  `année` year NOT NULL,
  `cylindrée` int NOT NULL,
  `puissance` float NOT NULL,
  `immatriculation` varchar(9) NOT NULL,
  `prix_neuf` float NOT NULL,
  `marque` int NOT NULL,
  PRIMARY KEY (`idMoto`),
  KEY `marque` (`marque`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `idUsers` int NOT NULL AUTO_INCREMENT,
  `login` varchar(20) NOT NULL,
  `mdp` varchar(50) NOT NULL,
  PRIMARY KEY (`idUsers`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`idUsers`, `login`, `mdp`) VALUES
(1, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Structure de la table `ventes`
--

DROP TABLE IF EXISTS `ventes`;
CREATE TABLE IF NOT EXISTS `ventes` (
  `idVente` int NOT NULL AUTO_INCREMENT,
  `prix_occasion` float NOT NULL,
  `kilomètres` float NOT NULL,
  `moto` int NOT NULL,
  `lieuxVente` int NOT NULL,
  PRIMARY KEY (`idVente`),
  KEY `ventes` (`lieuxVente`),
  KEY `moto` (`moto`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `moto`
--
ALTER TABLE `moto`
  ADD CONSTRAINT `marque` FOREIGN KEY (`marque`) REFERENCES `marque` (`idMarque`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `ventes`
--
ALTER TABLE `ventes`
  ADD CONSTRAINT `moto` FOREIGN KEY (`moto`) REFERENCES `moto` (`idMoto`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ventes` FOREIGN KEY (`lieuxVente`) REFERENCES `lieux_de_vente` (`idLieux`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
