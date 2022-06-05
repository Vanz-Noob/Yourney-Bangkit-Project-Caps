/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     01/06/2022 08:21:19                          */
/*==============================================================*/


drop table if exists DESTINASI;

drop table if exists GAMBAR;

drop table if exists KATEGORI;

drop table if exists OUTPUT;

drop table if exists USER;

/*==============================================================*/
/* Table: DESTINASI                                             */
/*==============================================================*/
create table DESTINASI
(
   ID_DESTINASI         int(20) not null auto_increment,
   ID_KATEGORI          int(20),
   NAMA_DESTINASI       varchar(50),
   DESKRIPSI            varchar(50),
   primary key (ID_DESTINASI)
);

/*==============================================================*/
/* Table: GAMBAR                                                */
/*==============================================================*/
create table GAMBAR
(
   ID_GAMBAR            int(20) not null auto_increment,
   ID_DESTINASI         int(20),
   URL_GAMBAR           varchar(50),
   primary key (ID_GAMBAR)
);

/*==============================================================*/
/* Table: KATEGORI                                              */
/*==============================================================*/
create table KATEGORI
(
   ID_KATEGORI          int(20) not null auto_increment,
   NAMA_KATEGORI        varchar(50),
   primary key (ID_KATEGORI)
);

/*==============================================================*/
/* Table: OUTPUT                                                */
/*==============================================================*/
create table OUTPUT
(
   ID_OUTPUT            int(20) not null auto_increment,
   ID_USER              int,
   ID_DESTINASI         int(20),
   primary key (ID_OUTPUT)
);

/*==============================================================*/
/* Table: USER                                                  */
/*==============================================================*/
create table USER
(
   ID_USER              int(100) not null auto_increment,
   USERNAME             varchar(50),
   PASSWORD             varchar(50),
   primary key (ID_USER)
);

alter table DESTINASI add constraint FK_REFERENCE_4 foreign key (ID_KATEGORI)
      references KATEGORI (ID_KATEGORI) on delete restrict on update cascade;

alter table GAMBAR add constraint FK_REFERENCE_3 foreign key (ID_DESTINASI)
      references DESTINASI (ID_DESTINASI) on delete restrict on update cascade;

alter table OUTPUT add constraint FK_REFERENCE_1 foreign key (ID_USER)
      references USER (ID_USER) on delete restrict on update cascade;

alter table OUTPUT add constraint FK_REFERENCE_2 foreign key (ID_DESTINASI)
      references DESTINASI (ID_DESTINASI) on delete restrict on update cascade;

