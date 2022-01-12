-- MySQL Script generated by MySQL Workbench
-- Wed 12 Jan 2022 03:51:12 PM CET
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema priprema
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema priprema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `priprema` DEFAULT CHARACTER SET utf8 ;
USE `priprema` ;

-- -----------------------------------------------------
-- Table `priprema`.`korisnik`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `priprema`.`korisnik` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(50) NOT NULL,
  `password` VARCHAR(50) NOT NULL,
  `vrsta_korisnika` INT NOT NULL,
  `godina_rodjenja` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;