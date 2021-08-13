-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema pos
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema pos
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `pos` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `pos` ;

-- -----------------------------------------------------
-- Table `pos`.`brand`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`brand` (
  `brandkey` INT NOT NULL AUTO_INCREMENT,
  `brandname` VARCHAR(45) NOT NULL,
  `brandid` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`brandkey`))
ENGINE = InnoDB
AUTO_INCREMENT = 26
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`category` (
  `categorykey` INT NOT NULL AUTO_INCREMENT,
  `categoryname` VARCHAR(45) NOT NULL,
  `categoryid` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`categorykey`),
  UNIQUE INDEX `idcategory_UNIQUE` (`categorykey` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 18
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`customer` (
  `customerkey` INT NOT NULL AUTO_INCREMENT,
  `customerid` VARCHAR(45) NULL DEFAULT NULL,
  `customername` VARCHAR(45) NULL DEFAULT NULL,
  `usersessionid` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`customerkey`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`goodsissue`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`goodsissue` (
  `goodsissuekey` INT NOT NULL AUTO_INCREMENT,
  `goodsissuedate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `usersessionid` VARCHAR(45) NULL DEFAULT NULL,
  `goodsissuetotal` DECIMAL(10,2) NOT NULL,
  `userkey` INT NOT NULL,
  `warehousekey` INT NOT NULL,
  `reason` VARCHAR(45) NULL DEFAULT NULL,
  `created` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`goodsissuekey`))
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`goodsissuedetail`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`goodsissuedetail` (
  `goodsissuedetailkey` INT NOT NULL AUTO_INCREMENT,
  `goodsissuekey` INT NOT NULL,
  `productkey` INT NOT NULL,
  `saleprice` DECIMAL(6,2) NOT NULL,
  `quantity` INT NOT NULL,
  `linetotal` DECIMAL(10,2) NOT NULL,
  `productname` VARCHAR(45) NOT NULL,
  `barcode` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`goodsissuedetailkey`))
ENGINE = InnoDB
AUTO_INCREMENT = 14
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`goodsreceipt`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`goodsreceipt` (
  `goodsreceiptkey` INT NOT NULL AUTO_INCREMENT,
  `userkey` INT NOT NULL,
  `warehousekey` INT NOT NULL,
  `receiptdate` DATETIME NULL DEFAULT NULL,
  `reason` VARCHAR(45) NULL DEFAULT NULL,
  `goodsreceipttotal` DECIMAL(10,2) NULL DEFAULT NULL,
  `usersessionid` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`goodsreceiptkey`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`goodsreceiptdetail`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`goodsreceiptdetail` (
  `goodsreceiptdetailkey` INT NOT NULL AUTO_INCREMENT,
  `goodsreceiptkey` INT NOT NULL,
  `productkey` INT NOT NULL,
  `warehousekey` INT NOT NULL,
  `quantity` INT NULL DEFAULT NULL,
  `purchaseprice` DECIMAL(10,2) NULL DEFAULT NULL,
  `linetotal` DECIMAL(10,2) NULL DEFAULT NULL,
  `productname` VARCHAR(45) NULL DEFAULT NULL,
  `barcode` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`goodsreceiptdetailkey`))
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`grpo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`grpo` (
  `grpokey` INT NOT NULL AUTO_INCREMENT,
  `vendorkey` INT NOT NULL,
  `userkey` INT NOT NULL,
  `warehousekey` INT NOT NULL,
  `receiptdate` DATETIME NULL DEFAULT NULL,
  `orderdate` DATETIME NULL DEFAULT NULL,
  `status` VARCHAR(1) NULL DEFAULT NULL,
  `grpototal` DECIMAL(10,2) NULL DEFAULT NULL,
  `usersessionid` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`grpokey`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`grpodetail`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`grpodetail` (
  `grpodetailkey` INT NOT NULL AUTO_INCREMENT,
  `grpokey` INT NOT NULL,
  `productkey` INT NOT NULL,
  `warehousekey` INT NOT NULL,
  `quantity` INT NULL DEFAULT NULL,
  `purchaseprice` DECIMAL(10,2) NULL DEFAULT NULL,
  `linetotal` DECIMAL(10,2) NULL DEFAULT NULL,
  `productname` VARCHAR(45) NULL DEFAULT NULL,
  `barcode` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`grpodetailkey`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`inventory`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`inventory` (
  `inventorykey` INT NOT NULL AUTO_INCREMENT,
  `productkey` INT NOT NULL,
  `warehousekey` INT NOT NULL,
  `onhandquantity` INT NULL DEFAULT NULL,
  PRIMARY KEY (`inventorykey`))
ENGINE = InnoDB
AUTO_INCREMENT = 13
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`pos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`pos` (
  `poskey` INT NOT NULL AUTO_INCREMENT,
  `posid` VARCHAR(45) NULL DEFAULT NULL,
  `posname` VARCHAR(45) NOT NULL,
  `storekey` VARCHAR(45) NOT NULL,
  `created` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `active` TINYINT(1) NULL DEFAULT '1',
  `deleted` TINYINT(1) NULL DEFAULT '0',
  PRIMARY KEY (`poskey`))
ENGINE = InnoDB
AUTO_INCREMENT = 15
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`product` (
  `productkey` INT NOT NULL AUTO_INCREMENT,
  `productname` VARCHAR(45) NOT NULL,
  `brandkey` INT NOT NULL,
  `barcode` VARCHAR(45) NOT NULL,
  `saleprice` DECIMAL(8,2) NOT NULL,
  `categorykey` INT NOT NULL,
  `vendorkey` INT NOT NULL,
  `productid` VARCHAR(45) NULL DEFAULT NULL,
  `usersessionid` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`productkey`),
  UNIQUE INDEX `barcode_UNIQUE` (`barcode` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`refundorder`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`refundorder` (
  `refundorderkey` INT NOT NULL AUTO_INCREMENT,
  `saleorderkey` INT NOT NULL,
  `refundorderdate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `usersessionid` VARCHAR(45) NOT NULL,
  `refundordertotal` DECIMAL(10,2) NOT NULL,
  `storekey` INT NOT NULL,
  `poskey` INT NOT NULL,
  `userkey` INT NOT NULL,
  `warehousekey` INT NOT NULL,
  `customerkey` INT NOT NULL,
  PRIMARY KEY (`refundorderkey`))
ENGINE = InnoDB
AUTO_INCREMENT = 10
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`refundorderdetail`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`refundorderdetail` (
  `refundorderdetailkey` INT NOT NULL AUTO_INCREMENT,
  `refundorderkey` INT NOT NULL,
  `productkey` INT NOT NULL,
  `saleprice` DECIMAL(6,2) NOT NULL,
  `quantity` INT NOT NULL,
  `linetotal` DECIMAL(10,2) NOT NULL,
  `productname` VARCHAR(45) NOT NULL,
  `barcode` VARCHAR(45) NOT NULL,
  `warehousekey` INT NOT NULL,
  PRIMARY KEY (`refundorderdetailkey`),
  UNIQUE INDEX `refundorderdetailkey_UNIQUE` (`refundorderdetailkey` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`saleorder`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`saleorder` (
  `saleorderkey` INT NOT NULL AUTO_INCREMENT,
  `saleorderdate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `usersessionid` VARCHAR(45) NULL DEFAULT NULL,
  `saleordertotal` DECIMAL(10,2) NOT NULL,
  `storekey` INT NOT NULL,
  `poskey` INT NOT NULL,
  `userkey` INT NOT NULL,
  `warehousekey` INT NOT NULL,
  `customerkey` INT NOT NULL,
  `created` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`saleorderkey`),
  UNIQUE INDEX `salekey_UNIQUE` (`saleorderkey` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`saleorderdetail`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`saleorderdetail` (
  `saleorderdetailkey` INT NOT NULL AUTO_INCREMENT,
  `saleorderkey` INT NOT NULL,
  `productkey` INT NOT NULL,
  `saleprice` DECIMAL(6,2) NOT NULL,
  `quantity` INT NOT NULL,
  `linetotal` DECIMAL(10,2) NOT NULL,
  `productname` VARCHAR(45) NOT NULL,
  `barcode` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`saleorderdetailkey`))
ENGINE = InnoDB
AUTO_INCREMENT = 13
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`store`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`store` (
  `storekey` INT NOT NULL AUTO_INCREMENT,
  `storeid` VARCHAR(45) NULL DEFAULT NULL,
  `storename` VARCHAR(45) NOT NULL,
  `active` TINYINT(1) NULL DEFAULT '1',
  `deleted` TINYINT(1) NULL DEFAULT '0',
  `warehousekey` INT NOT NULL,
  `created` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `defaultcustomerkey` INT NOT NULL,
  PRIMARY KEY (`storekey`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`user` (
  `userkey` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `userpassword` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`userkey`),
  UNIQUE INDEX `useremail_UNIQUE` (`username` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`userstore`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`userstore` (
  `userstoreskey` INT NOT NULL AUTO_INCREMENT,
  `userkey` INT NOT NULL,
  `storekey` INT NOT NULL,
  `poskey` INT NOT NULL,
  PRIMARY KEY (`userstoreskey`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`vendor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`vendor` (
  `vendorkey` INT NOT NULL AUTO_INCREMENT,
  `vendorname` VARCHAR(45) NULL DEFAULT NULL,
  `vendorid` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`vendorkey`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pos`.`warehouse`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pos`.`warehouse` (
  `warehousekey` INT NOT NULL AUTO_INCREMENT,
  `warehouseid` VARCHAR(45) NULL DEFAULT NULL,
  `warehousename` VARCHAR(45) NOT NULL,
  `active` TINYINT(1) NULL DEFAULT '1',
  `deleted` TINYINT(1) NULL DEFAULT '0',
  PRIMARY KEY (`warehousekey`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
