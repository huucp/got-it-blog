-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema got-it-blog
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema got-it-blog
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `got-it-blog` DEFAULT CHARACTER SET utf8 ;
USE `got-it-blog` ;

-- -----------------------------------------------------
-- Table `got-it-blog`.`user_info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `got-it-blog`.`user_info` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(128) NOT NULL,
  `user_type` VARCHAR(8) NOT NULL,
  `user_name` VARCHAR(1024) NULL,
  `user_phone` VARCHAR(32) NULL,
  `user_job_type` VARCHAR(32) NULL,
  `user_job_other` VARCHAR(512) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unique_user_id` (`user_id` ) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `got-it-blog`.`blog`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `got-it-blog`.`blog` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(128) NOT NULL,
  `title` VARCHAR(2048) NOT NULL,
  `content` TEXT NULL,
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id` ) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `got-it-blog`.`like_tbl`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `got-it-blog`.`like_tbl` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(128) NULL,
  `blog_id` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_blog_id_idx` (`blog_id` ) ,
  UNIQUE INDEX `one_like_index` (`user_id` ASC, `blog_id` ) ,
  CONSTRAINT `fk_blog_id`
    FOREIGN KEY (`blog_id`)
    REFERENCES `got-it-blog`.`blog` (`id`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
