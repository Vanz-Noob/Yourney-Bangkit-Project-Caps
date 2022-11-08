-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema yourney
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `yourney` ;

-- -----------------------------------------------------
-- Schema yourney
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `yourney` DEFAULT CHARACTER SET utf8 ;
-- -----------------------------------------------------
-- Schema yourney
-- -----------------------------------------------------
USE `yourney` ;

-- -----------------------------------------------------
-- Table `yourney`.`dataset`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `yourney`.`dataset` ;

CREATE TABLE IF NOT EXISTS `yourney`.`dataset` (
  `id_dataset` INT NOT NULL AUTO_INCREMENT,
  `id_kategori3` INT NULL,
  `cleaned_tweet` VARCHAR(255) NULL,
  PRIMARY KEY (`id_dataset`),
  CONSTRAINT `id_kategori3`
    FOREIGN KEY (`id_kategori3`)
    REFERENCES `yourney`.`kategori` (`id_kategori_user`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE INDEX `id_kategori3_idx` ON `yourney`.`dataset` (`id_kategori3` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `yourney`.`destinasi`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `yourney`.`destinasi` ;

CREATE TABLE IF NOT EXISTS `yourney`.`destinasi` (
  `id_destinasi` INT NOT NULL AUTO_INCREMENT,
  `id_kategori2` INT NULL,
  `nama_destinasi` VARCHAR(255) NOT NULL,
  `deskripsi` TEXT NULL,
  `pic_destinasi` VARCHAR(255) NULL,
  PRIMARY KEY (`id_destinasi`),
  CONSTRAINT `id_kategori2`
    FOREIGN KEY (`id_kategori2`)
    REFERENCES `yourney`.`kategori` (`id_kategori_user`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE INDEX `id_kategori2_idx` ON `yourney`.`destinasi` (`id_kategori2` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `yourney`.`kategori`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `yourney`.`kategori` ;

CREATE TABLE IF NOT EXISTS `yourney`.`kategori` (
  `id_kategori_user` INT NOT NULL,
  `id_kategori` INT NULL DEFAULT NULL,
  `id_dataset1` INT NULL DEFAULT NULL,
  `id_destinasi1` INT NULL DEFAULT NULL,
  `nama_kategori` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id_kategori_user`),
  CONSTRAINT `id_dataset1`
    FOREIGN KEY (`id_dataset1`)
    REFERENCES `yourney`.`dataset` (`id_dataset`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id_destinasi1`
    FOREIGN KEY (`id_destinasi1`)
    REFERENCES `yourney`.`destinasi` (`id_destinasi`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE INDEX `id_dataset1_idx` ON `yourney`.`kategori` (`id_dataset1` ASC) VISIBLE;

CREATE INDEX `id_destinasi1_idx` ON `yourney`.`kategori` (`id_destinasi1` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `yourney`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `yourney`.`user` ;

CREATE TABLE IF NOT EXISTS `yourney`.`user` (
  `id_user` INT NOT NULL AUTO_INCREMENT,
  `id_kategori1` INT NULL,
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `jenis_kelamin` VARCHAR(255) NULL DEFAULT NULL,
  `tempatlahir` VARCHAR(255) NULL DEFAULT NULL,
  `status` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id_user`),
  CONSTRAINT `id_kategori1`
    FOREIGN KEY (`id_kategori1`)
    REFERENCES `yourney`.`kategori` (`id_kategori_user`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE INDEX `id_kategori1_idx` ON `yourney`.`user` (`id_kategori1` ASC) VISIBLE;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
