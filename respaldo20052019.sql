PGDMP             	            w           prueba1    11.2    11.2 �               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false                       1262    44004    prueba1    DATABASE     �   CREATE DATABASE prueba1 WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Spanish_Mexico.1252' LC_CTYPE = 'Spanish_Mexico.1252';
    DROP DATABASE prueba1;
             postgres    false            �            1259    44036 
   auth_group    TABLE     f   CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);
    DROP TABLE public.auth_group;
       public         postgres    false            �            1259    44034    auth_group_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.auth_group_id_seq;
       public       postgres    false    203                       0    0    auth_group_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;
            public       postgres    false    202            �            1259    44046    auth_group_permissions    TABLE     �   CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);
 *   DROP TABLE public.auth_group_permissions;
       public         postgres    false            �            1259    44044    auth_group_permissions_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.auth_group_permissions_id_seq;
       public       postgres    false    205                       0    0    auth_group_permissions_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;
            public       postgres    false    204            �            1259    44028    auth_permission    TABLE     �   CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);
 #   DROP TABLE public.auth_permission;
       public         postgres    false            �            1259    44026    auth_permission_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.auth_permission_id_seq;
       public       postgres    false    201                       0    0    auth_permission_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;
            public       postgres    false    200            �            1259    44054 	   auth_user    TABLE     �  CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);
    DROP TABLE public.auth_user;
       public         postgres    false            �            1259    44064    auth_user_groups    TABLE        CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);
 $   DROP TABLE public.auth_user_groups;
       public         postgres    false            �            1259    44062    auth_user_groups_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.auth_user_groups_id_seq;
       public       postgres    false    209            	           0    0    auth_user_groups_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;
            public       postgres    false    208            �            1259    44052    auth_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.auth_user_id_seq;
       public       postgres    false    207            
           0    0    auth_user_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;
            public       postgres    false    206            �            1259    44072    auth_user_user_permissions    TABLE     �   CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);
 .   DROP TABLE public.auth_user_user_permissions;
       public         postgres    false            �            1259    44070 !   auth_user_user_permissions_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE public.auth_user_user_permissions_id_seq;
       public       postgres    false    211                       0    0 !   auth_user_user_permissions_id_seq    SEQUENCE OWNED BY     g   ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;
            public       postgres    false    210            �            1259    44189    dependencia_departamento    TABLE     �   CREATE TABLE public.dependencia_departamento (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    encargado character varying(100) NOT NULL,
    dependencia_id integer NOT NULL
);
 ,   DROP TABLE public.dependencia_departamento;
       public         postgres    false            �            1259    44187    dependencia_departamento_id_seq    SEQUENCE     �   CREATE SEQUENCE public.dependencia_departamento_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 6   DROP SEQUENCE public.dependencia_departamento_id_seq;
       public       postgres    false    219                       0    0    dependencia_departamento_id_seq    SEQUENCE OWNED BY     c   ALTER SEQUENCE public.dependencia_departamento_id_seq OWNED BY public.dependencia_departamento.id;
            public       postgres    false    218            �            1259    44173    dependencia_dependencia    TABLE     B  CREATE TABLE public.dependencia_dependencia (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    director character varying(100) NOT NULL,
    direccion character varying(100) NOT NULL,
    telefono character varying(100) NOT NULL,
    tipo character varying(30) NOT NULL,
    adscrita_id integer
);
 +   DROP TABLE public.dependencia_dependencia;
       public         postgres    false            �            1259    44171    dependencia_dependencia_id_seq    SEQUENCE     �   CREATE SEQUENCE public.dependencia_dependencia_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.dependencia_dependencia_id_seq;
       public       postgres    false    217                       0    0    dependencia_dependencia_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.dependencia_dependencia_id_seq OWNED BY public.dependencia_dependencia.id;
            public       postgres    false    216            �            1259    44165    dependencia_raiz    TABLE     =  CREATE TABLE public.dependencia_raiz (
    id integer NOT NULL,
    nombre character varying(100),
    tipo character varying(30) NOT NULL,
    responsable character varying(100),
    telefono character varying(100) NOT NULL,
    direccion character varying(100) NOT NULL,
    estado character varying(5) NOT NULL
);
 $   DROP TABLE public.dependencia_raiz;
       public         postgres    false            �            1259    44163    dependencia_raiz_id_seq    SEQUENCE     �   CREATE SEQUENCE public.dependencia_raiz_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.dependencia_raiz_id_seq;
       public       postgres    false    215                       0    0    dependencia_raiz_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.dependencia_raiz_id_seq OWNED BY public.dependencia_raiz.id;
            public       postgres    false    214            �            1259    44132    django_admin_log    TABLE     �  CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);
 $   DROP TABLE public.django_admin_log;
       public         postgres    false            �            1259    44130    django_admin_log_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.django_admin_log_id_seq;
       public       postgres    false    213                       0    0    django_admin_log_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;
            public       postgres    false    212            �            1259    44018    django_content_type    TABLE     �   CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);
 '   DROP TABLE public.django_content_type;
       public         postgres    false            �            1259    44016    django_content_type_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.django_content_type_id_seq;
       public       postgres    false    199                       0    0    django_content_type_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;
            public       postgres    false    198            �            1259    44007    django_migrations    TABLE     �   CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);
 %   DROP TABLE public.django_migrations;
       public         postgres    false            �            1259    44005    django_migrations_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.django_migrations_id_seq;
       public       postgres    false    197                       0    0    django_migrations_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;
            public       postgres    false    196            �            1259    44317    django_session    TABLE     �   CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);
 "   DROP TABLE public.django_session;
       public         postgres    false            �            1259    44217    objetivo_objetivo    TABLE     �  CREATE TABLE public.objetivo_objetivo (
    id integer NOT NULL,
    numero character varying(300) NOT NULL,
    nombre character varying(300) NOT NULL,
    tipo character varying(300) NOT NULL,
    descripcion character varying(1000) NOT NULL,
    meta character varying(200) NOT NULL,
    estrategia character varying(1000) NOT NULL,
    "ejeTransversal" character varying(300) NOT NULL
);
 %   DROP TABLE public.objetivo_objetivo;
       public         postgres    false            �            1259    44367    objetivo_objetivo_dependencia    TABLE     �   CREATE TABLE public.objetivo_objetivo_dependencia (
    id integer NOT NULL,
    objetivo_id integer NOT NULL,
    dependencia_id integer NOT NULL
);
 1   DROP TABLE public.objetivo_objetivo_dependencia;
       public         postgres    false            �            1259    44365 $   objetivo_objetivo_dependencia_id_seq    SEQUENCE     �   CREATE SEQUENCE public.objetivo_objetivo_dependencia_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ;   DROP SEQUENCE public.objetivo_objetivo_dependencia_id_seq;
       public       postgres    false    232                       0    0 $   objetivo_objetivo_dependencia_id_seq    SEQUENCE OWNED BY     m   ALTER SEQUENCE public.objetivo_objetivo_dependencia_id_seq OWNED BY public.objetivo_objetivo_dependencia.id;
            public       postgres    false    231            �            1259    44215    objetivo_objetivo_id_seq    SEQUENCE     �   CREATE SEQUENCE public.objetivo_objetivo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.objetivo_objetivo_id_seq;
       public       postgres    false    221                       0    0    objetivo_objetivo_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.objetivo_objetivo_id_seq OWNED BY public.objetivo_objetivo.id;
            public       postgres    false    220            �            1259    44296    programaOperativo_actividad    TABLE     �  CREATE TABLE public."programaOperativo_actividad" (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text NOT NULL,
    fecha_in date NOT NULL,
    fecha_fi date NOT NULL,
    programaoperativo_id integer NOT NULL,
    user_id integer NOT NULL,
    evidencia character varying(100),
    "personasInvolucradas" character varying(10),
    "presupuestoEjercido" character varying(300),
    "presupuestoProgramado" character varying(300) NOT NULL
);
 1   DROP TABLE public."programaOperativo_actividad";
       public         postgres    false            �            1259    44294 #   programaOperativo_actividad_id_seq1    SEQUENCE     �   CREATE SEQUENCE public."programaOperativo_actividad_id_seq1"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 <   DROP SEQUENCE public."programaOperativo_actividad_id_seq1";
       public       postgres    false    225                       0    0 #   programaOperativo_actividad_id_seq1    SEQUENCE OWNED BY     n   ALTER SEQUENCE public."programaOperativo_actividad_id_seq1" OWNED BY public."programaOperativo_actividad".id;
            public       postgres    false    224            �            1259    44250 #   programaOperativo_programaoperativo    TABLE     .  CREATE TABLE public."programaOperativo_programaoperativo" (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion character varying(600) NOT NULL,
    "tipoPrograma" character varying(30) NOT NULL,
    objetivos character varying(600) NOT NULL,
    estrategias character varying(600) NOT NULL,
    beneficiarios character varying(600) NOT NULL,
    justificacion character varying(600) NOT NULL,
    "problematicaSocial" character varying(600) NOT NULL,
    dependencia_id integer NOT NULL,
    objetivo_id integer NOT NULL
);
 9   DROP TABLE public."programaOperativo_programaoperativo";
       public         postgres    false            �            1259    44248 *   programaOperativo_programaoperativo_id_seq    SEQUENCE     �   CREATE SEQUENCE public."programaOperativo_programaoperativo_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 C   DROP SEQUENCE public."programaOperativo_programaoperativo_id_seq";
       public       postgres    false    223                       0    0 *   programaOperativo_programaoperativo_id_seq    SEQUENCE OWNED BY     }   ALTER SEQUENCE public."programaOperativo_programaoperativo_id_seq" OWNED BY public."programaOperativo_programaoperativo".id;
            public       postgres    false    222            �            1259    44329    users_persona    TABLE     �   CREATE TABLE public.users_persona (
    id integer NOT NULL,
    nombre character varying(30) NOT NULL,
    apellidopaterno character varying(30) NOT NULL,
    apellidomaterno character varying(30) NOT NULL,
    edad integer NOT NULL
);
 !   DROP TABLE public.users_persona;
       public         postgres    false            �            1259    44327    users_persona_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_persona_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.users_persona_id_seq;
       public       postgres    false    228                       0    0    users_persona_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.users_persona_id_seq OWNED BY public.users_persona.id;
            public       postgres    false    227            �            1259    44337    users_profile    TABLE       CREATE TABLE public.users_profile (
    id integer NOT NULL,
    telephone character varying(30) NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    dependencia_id integer,
    user_id integer NOT NULL
);
 !   DROP TABLE public.users_profile;
       public         postgres    false            �            1259    44335    users_profile_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_profile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.users_profile_id_seq;
       public       postgres    false    230                       0    0    users_profile_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.users_profile_id_seq OWNED BY public.users_profile.id;
            public       postgres    false    229            �
           2604    44039    auth_group id    DEFAULT     n   ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);
 <   ALTER TABLE public.auth_group ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    203    202    203            �
           2604    44049    auth_group_permissions id    DEFAULT     �   ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);
 H   ALTER TABLE public.auth_group_permissions ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    204    205    205            �
           2604    44031    auth_permission id    DEFAULT     x   ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);
 A   ALTER TABLE public.auth_permission ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    201    200    201            �
           2604    44057    auth_user id    DEFAULT     l   ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);
 ;   ALTER TABLE public.auth_user ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    206    207    207            �
           2604    44067    auth_user_groups id    DEFAULT     z   ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);
 B   ALTER TABLE public.auth_user_groups ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    208    209    209            �
           2604    44075    auth_user_user_permissions id    DEFAULT     �   ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);
 L   ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    211    210    211            �
           2604    44192    dependencia_departamento id    DEFAULT     �   ALTER TABLE ONLY public.dependencia_departamento ALTER COLUMN id SET DEFAULT nextval('public.dependencia_departamento_id_seq'::regclass);
 J   ALTER TABLE public.dependencia_departamento ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    218    219    219            �
           2604    44176    dependencia_dependencia id    DEFAULT     �   ALTER TABLE ONLY public.dependencia_dependencia ALTER COLUMN id SET DEFAULT nextval('public.dependencia_dependencia_id_seq'::regclass);
 I   ALTER TABLE public.dependencia_dependencia ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    217    216    217            �
           2604    44168    dependencia_raiz id    DEFAULT     z   ALTER TABLE ONLY public.dependencia_raiz ALTER COLUMN id SET DEFAULT nextval('public.dependencia_raiz_id_seq'::regclass);
 B   ALTER TABLE public.dependencia_raiz ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    214    215    215            �
           2604    44135    django_admin_log id    DEFAULT     z   ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);
 B   ALTER TABLE public.django_admin_log ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    212    213    213            �
           2604    44021    django_content_type id    DEFAULT     �   ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);
 E   ALTER TABLE public.django_content_type ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    199    198    199            �
           2604    44010    django_migrations id    DEFAULT     |   ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);
 C   ALTER TABLE public.django_migrations ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    196    197    197            �
           2604    44220    objetivo_objetivo id    DEFAULT     |   ALTER TABLE ONLY public.objetivo_objetivo ALTER COLUMN id SET DEFAULT nextval('public.objetivo_objetivo_id_seq'::regclass);
 C   ALTER TABLE public.objetivo_objetivo ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    220    221    221                        2604    44370     objetivo_objetivo_dependencia id    DEFAULT     �   ALTER TABLE ONLY public.objetivo_objetivo_dependencia ALTER COLUMN id SET DEFAULT nextval('public.objetivo_objetivo_dependencia_id_seq'::regclass);
 O   ALTER TABLE public.objetivo_objetivo_dependencia ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    231    232    232            �
           2604    44299    programaOperativo_actividad id    DEFAULT     �   ALTER TABLE ONLY public."programaOperativo_actividad" ALTER COLUMN id SET DEFAULT nextval('public."programaOperativo_actividad_id_seq1"'::regclass);
 O   ALTER TABLE public."programaOperativo_actividad" ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    225    224    225            �
           2604    44253 &   programaOperativo_programaoperativo id    DEFAULT     �   ALTER TABLE ONLY public."programaOperativo_programaoperativo" ALTER COLUMN id SET DEFAULT nextval('public."programaOperativo_programaoperativo_id_seq"'::regclass);
 W   ALTER TABLE public."programaOperativo_programaoperativo" ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    222    223    223            �
           2604    44332    users_persona id    DEFAULT     t   ALTER TABLE ONLY public.users_persona ALTER COLUMN id SET DEFAULT nextval('public.users_persona_id_seq'::regclass);
 ?   ALTER TABLE public.users_persona ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    227    228    228            �
           2604    44340    users_profile id    DEFAULT     t   ALTER TABLE ONLY public.users_profile ALTER COLUMN id SET DEFAULT nextval('public.users_profile_id_seq'::regclass);
 ?   ALTER TABLE public.users_profile ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    229    230    230            �          0    44036 
   auth_group 
   TABLE DATA               .   COPY public.auth_group (id, name) FROM stdin;
    public       postgres    false    203   ��       �          0    44046    auth_group_permissions 
   TABLE DATA               M   COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
    public       postgres    false    205   ��       �          0    44028    auth_permission 
   TABLE DATA               N   COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
    public       postgres    false    201   �       �          0    44054 	   auth_user 
   TABLE DATA               �   COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
    public       postgres    false    207          �          0    44064    auth_user_groups 
   TABLE DATA               A   COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
    public       postgres    false    209   �      �          0    44072    auth_user_user_permissions 
   TABLE DATA               P   COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
    public       postgres    false    211   $      �          0    44189    dependencia_departamento 
   TABLE DATA               Y   COPY public.dependencia_departamento (id, nombre, encargado, dependencia_id) FROM stdin;
    public       postgres    false    219         �          0    44173    dependencia_dependencia 
   TABLE DATA               o   COPY public.dependencia_dependencia (id, nombre, director, direccion, telefono, tipo, adscrita_id) FROM stdin;
    public       postgres    false    217   $      �          0    44165    dependencia_raiz 
   TABLE DATA               f   COPY public.dependencia_raiz (id, nombre, tipo, responsable, telefono, direccion, estado) FROM stdin;
    public       postgres    false    215   }      �          0    44132    django_admin_log 
   TABLE DATA               �   COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
    public       postgres    false    213   	      �          0    44018    django_content_type 
   TABLE DATA               C   COPY public.django_content_type (id, app_label, model) FROM stdin;
    public       postgres    false    199   �      �          0    44007    django_migrations 
   TABLE DATA               C   COPY public.django_migrations (id, app, name, applied) FROM stdin;
    public       postgres    false    197   u      �          0    44317    django_session 
   TABLE DATA               P   COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
    public       postgres    false    226         �          0    44217    objetivo_objetivo 
   TABLE DATA               v   COPY public.objetivo_objetivo (id, numero, nombre, tipo, descripcion, meta, estrategia, "ejeTransversal") FROM stdin;
    public       postgres    false    221   <      �          0    44367    objetivo_objetivo_dependencia 
   TABLE DATA               X   COPY public.objetivo_objetivo_dependencia (id, objetivo_id, dependencia_id) FROM stdin;
    public       postgres    false    232   �+      �          0    44296    programaOperativo_actividad 
   TABLE DATA               �   COPY public."programaOperativo_actividad" (id, nombre, descripcion, fecha_in, fecha_fi, programaoperativo_id, user_id, evidencia, "personasInvolucradas", "presupuestoEjercido", "presupuestoProgramado") FROM stdin;
    public       postgres    false    225   �,      �          0    44250 #   programaOperativo_programaoperativo 
   TABLE DATA               �   COPY public."programaOperativo_programaoperativo" (id, nombre, descripcion, "tipoPrograma", objetivos, estrategias, beneficiarios, justificacion, "problematicaSocial", dependencia_id, objetivo_id) FROM stdin;
    public       postgres    false    223   R-      �          0    44329    users_persona 
   TABLE DATA               [   COPY public.users_persona (id, nombre, apellidopaterno, apellidomaterno, edad) FROM stdin;
    public       postgres    false    228   �-      �          0    44337    users_profile 
   TABLE DATA               b   COPY public.users_profile (id, telephone, created, modified, dependencia_id, user_id) FROM stdin;
    public       postgres    false    230   �-                 0    0    auth_group_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.auth_group_id_seq', 2, true);
            public       postgres    false    202                       0    0    auth_group_permissions_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 80, true);
            public       postgres    false    204                       0    0    auth_permission_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.auth_permission_id_seq', 60, true);
            public       postgres    false    200                       0    0    auth_user_groups_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 2, true);
            public       postgres    false    208                       0    0    auth_user_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.auth_user_id_seq', 4, true);
            public       postgres    false    206                       0    0 !   auth_user_user_permissions_id_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 60, true);
            public       postgres    false    210                       0    0    dependencia_departamento_id_seq    SEQUENCE SET     N   SELECT pg_catalog.setval('public.dependencia_departamento_id_seq', 1, false);
            public       postgres    false    218                       0    0    dependencia_dependencia_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public.dependencia_dependencia_id_seq', 1, false);
            public       postgres    false    216                        0    0    dependencia_raiz_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.dependencia_raiz_id_seq', 1, false);
            public       postgres    false    214            !           0    0    django_admin_log_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.django_admin_log_id_seq', 123, true);
            public       postgres    false    212            "           0    0    django_content_type_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.django_content_type_id_seq', 15, true);
            public       postgres    false    198            #           0    0    django_migrations_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.django_migrations_id_seq', 32, true);
            public       postgres    false    196            $           0    0 $   objetivo_objetivo_dependencia_id_seq    SEQUENCE SET     S   SELECT pg_catalog.setval('public.objetivo_objetivo_dependencia_id_seq', 83, true);
            public       postgres    false    231            %           0    0    objetivo_objetivo_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.objetivo_objetivo_id_seq', 1, false);
            public       postgres    false    220            &           0    0 #   programaOperativo_actividad_id_seq1    SEQUENCE SET     S   SELECT pg_catalog.setval('public."programaOperativo_actividad_id_seq1"', 1, true);
            public       postgres    false    224            '           0    0 *   programaOperativo_programaoperativo_id_seq    SEQUENCE SET     Z   SELECT pg_catalog.setval('public."programaOperativo_programaoperativo_id_seq"', 1, true);
            public       postgres    false    222            (           0    0    users_persona_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.users_persona_id_seq', 1, false);
            public       postgres    false    227            )           0    0    users_profile_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.users_profile_id_seq', 3, true);
            public       postgres    false    229                       2606    44161    auth_group auth_group_name_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);
 H   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
       public         postgres    false    203                       2606    44098 R   auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);
 |   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
       public         postgres    false    205    205                       2606    44051 2   auth_group_permissions auth_group_permissions_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
       public         postgres    false    205                       2606    44041    auth_group auth_group_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
       public         postgres    false    203            	           2606    44084 F   auth_permission auth_permission_content_type_id_codename_01ab375a_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);
 p   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq;
       public         postgres    false    201    201                       2606    44033 $   auth_permission auth_permission_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
       public         postgres    false    201                       2606    44069 &   auth_user_groups auth_user_groups_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_pkey;
       public         postgres    false    209            !           2606    44113 @   auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);
 j   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq;
       public         postgres    false    209    209                       2606    44059    auth_user auth_user_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_pkey;
       public         postgres    false    207            $           2606    44077 :   auth_user_user_permissions auth_user_user_permissions_pkey 
   CONSTRAINT     x   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);
 d   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_pkey;
       public         postgres    false    211            '           2606    44127 Y   auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);
 �   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq;
       public         postgres    false    211    211                       2606    44155     auth_user auth_user_username_key 
   CONSTRAINT     _   ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);
 J   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_username_key;
       public         postgres    false    207            3           2606    44194 6   dependencia_departamento dependencia_departamento_pkey 
   CONSTRAINT     t   ALTER TABLE ONLY public.dependencia_departamento
    ADD CONSTRAINT dependencia_departamento_pkey PRIMARY KEY (id);
 `   ALTER TABLE ONLY public.dependencia_departamento DROP CONSTRAINT dependencia_departamento_pkey;
       public         postgres    false    219            0           2606    44178 4   dependencia_dependencia dependencia_dependencia_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY public.dependencia_dependencia
    ADD CONSTRAINT dependencia_dependencia_pkey PRIMARY KEY (id);
 ^   ALTER TABLE ONLY public.dependencia_dependencia DROP CONSTRAINT dependencia_dependencia_pkey;
       public         postgres    false    217            -           2606    44170 &   dependencia_raiz dependencia_raiz_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.dependencia_raiz
    ADD CONSTRAINT dependencia_raiz_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.dependencia_raiz DROP CONSTRAINT dependencia_raiz_pkey;
       public         postgres    false    215            *           2606    44141 &   django_admin_log django_admin_log_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
       public         postgres    false    213                       2606    44025 E   django_content_type django_content_type_app_label_model_76bd3d3b_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);
 o   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq;
       public         postgres    false    199    199                       2606    44023 ,   django_content_type django_content_type_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
       public         postgres    false    199                       2606    44015 (   django_migrations django_migrations_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.django_migrations DROP CONSTRAINT django_migrations_pkey;
       public         postgres    false    197            @           2606    44324 "   django_session django_session_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);
 L   ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
       public         postgres    false    226            J           2606    44384 ]   objetivo_objetivo_dependencia objetivo_objetivo_depend_objetivo_id_dependencia__ff6d1533_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.objetivo_objetivo_dependencia
    ADD CONSTRAINT objetivo_objetivo_depend_objetivo_id_dependencia__ff6d1533_uniq UNIQUE (objetivo_id, dependencia_id);
 �   ALTER TABLE ONLY public.objetivo_objetivo_dependencia DROP CONSTRAINT objetivo_objetivo_depend_objetivo_id_dependencia__ff6d1533_uniq;
       public         postgres    false    232    232            N           2606    44372 @   objetivo_objetivo_dependencia objetivo_objetivo_dependencia_pkey 
   CONSTRAINT     ~   ALTER TABLE ONLY public.objetivo_objetivo_dependencia
    ADD CONSTRAINT objetivo_objetivo_dependencia_pkey PRIMARY KEY (id);
 j   ALTER TABLE ONLY public.objetivo_objetivo_dependencia DROP CONSTRAINT objetivo_objetivo_dependencia_pkey;
       public         postgres    false    232            5           2606    44225 (   objetivo_objetivo objetivo_objetivo_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.objetivo_objetivo
    ADD CONSTRAINT objetivo_objetivo_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.objetivo_objetivo DROP CONSTRAINT objetivo_objetivo_pkey;
       public         postgres    false    221            ;           2606    44304 =   programaOperativo_actividad programaOperativo_actividad_pkey1 
   CONSTRAINT        ALTER TABLE ONLY public."programaOperativo_actividad"
    ADD CONSTRAINT "programaOperativo_actividad_pkey1" PRIMARY KEY (id);
 k   ALTER TABLE ONLY public."programaOperativo_actividad" DROP CONSTRAINT "programaOperativo_actividad_pkey1";
       public         postgres    false    225            9           2606    44258 L   programaOperativo_programaoperativo programaOperativo_programaoperativo_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public."programaOperativo_programaoperativo"
    ADD CONSTRAINT "programaOperativo_programaoperativo_pkey" PRIMARY KEY (id);
 z   ALTER TABLE ONLY public."programaOperativo_programaoperativo" DROP CONSTRAINT "programaOperativo_programaoperativo_pkey";
       public         postgres    false    223            C           2606    44334     users_persona users_persona_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.users_persona
    ADD CONSTRAINT users_persona_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.users_persona DROP CONSTRAINT users_persona_pkey;
       public         postgres    false    228            F           2606    44342     users_profile users_profile_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.users_profile
    ADD CONSTRAINT users_profile_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.users_profile DROP CONSTRAINT users_profile_pkey;
       public         postgres    false    230            H           2606    44344 '   users_profile users_profile_user_id_key 
   CONSTRAINT     e   ALTER TABLE ONLY public.users_profile
    ADD CONSTRAINT users_profile_user_id_key UNIQUE (user_id);
 Q   ALTER TABLE ONLY public.users_profile DROP CONSTRAINT users_profile_user_id_key;
       public         postgres    false    230                       1259    44162    auth_group_name_a6ea08ec_like    INDEX     h   CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);
 1   DROP INDEX public.auth_group_name_a6ea08ec_like;
       public         postgres    false    203                       1259    44099 (   auth_group_permissions_group_id_b120cbf9    INDEX     o   CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);
 <   DROP INDEX public.auth_group_permissions_group_id_b120cbf9;
       public         postgres    false    205                       1259    44100 -   auth_group_permissions_permission_id_84c5c92e    INDEX     y   CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);
 A   DROP INDEX public.auth_group_permissions_permission_id_84c5c92e;
       public         postgres    false    205                       1259    44085 (   auth_permission_content_type_id_2f476e4b    INDEX     o   CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);
 <   DROP INDEX public.auth_permission_content_type_id_2f476e4b;
       public         postgres    false    201                       1259    44115 "   auth_user_groups_group_id_97559544    INDEX     c   CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);
 6   DROP INDEX public.auth_user_groups_group_id_97559544;
       public         postgres    false    209                       1259    44114 !   auth_user_groups_user_id_6a12ed8b    INDEX     a   CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);
 5   DROP INDEX public.auth_user_groups_user_id_6a12ed8b;
       public         postgres    false    209            "           1259    44129 1   auth_user_user_permissions_permission_id_1fbb5f2c    INDEX     �   CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);
 E   DROP INDEX public.auth_user_user_permissions_permission_id_1fbb5f2c;
       public         postgres    false    211            %           1259    44128 +   auth_user_user_permissions_user_id_a95ead1b    INDEX     u   CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);
 ?   DROP INDEX public.auth_user_user_permissions_user_id_a95ead1b;
       public         postgres    false    211                       1259    44156     auth_user_username_6821ab7c_like    INDEX     n   CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);
 4   DROP INDEX public.auth_user_username_6821ab7c_like;
       public         postgres    false    207            1           1259    44214 0   dependencia_departamento_dependencia_id_8bce7a3e    INDEX        CREATE INDEX dependencia_departamento_dependencia_id_8bce7a3e ON public.dependencia_departamento USING btree (dependencia_id);
 D   DROP INDEX public.dependencia_departamento_dependencia_id_8bce7a3e;
       public         postgres    false    219            .           1259    44358 ,   dependencia_dependencia_adscrita_id_3b7c8390    INDEX     w   CREATE INDEX dependencia_dependencia_adscrita_id_3b7c8390 ON public.dependencia_dependencia USING btree (adscrita_id);
 @   DROP INDEX public.dependencia_dependencia_adscrita_id_3b7c8390;
       public         postgres    false    217            (           1259    44152 )   django_admin_log_content_type_id_c4bce8eb    INDEX     q   CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);
 =   DROP INDEX public.django_admin_log_content_type_id_c4bce8eb;
       public         postgres    false    213            +           1259    44153 !   django_admin_log_user_id_c564eba6    INDEX     a   CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);
 5   DROP INDEX public.django_admin_log_user_id_c564eba6;
       public         postgres    false    213            >           1259    44326 #   django_session_expire_date_a5c62663    INDEX     e   CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);
 7   DROP INDEX public.django_session_expire_date_a5c62663;
       public         postgres    false    226            A           1259    44325 (   django_session_session_key_c0390e0f_like    INDEX     ~   CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);
 <   DROP INDEX public.django_session_session_key_c0390e0f_like;
       public         postgres    false    226            K           1259    44386 5   objetivo_objetivo_dependencia_dependencia_id_c4bd31b7    INDEX     �   CREATE INDEX objetivo_objetivo_dependencia_dependencia_id_c4bd31b7 ON public.objetivo_objetivo_dependencia USING btree (dependencia_id);
 I   DROP INDEX public.objetivo_objetivo_dependencia_dependencia_id_c4bd31b7;
       public         postgres    false    232            L           1259    44385 2   objetivo_objetivo_dependencia_objetivo_id_ce277155    INDEX     �   CREATE INDEX objetivo_objetivo_dependencia_objetivo_id_ce277155 ON public.objetivo_objetivo_dependencia USING btree (objetivo_id);
 F   DROP INDEX public.objetivo_objetivo_dependencia_objetivo_id_ce277155;
       public         postgres    false    232            <           1259    44315 9   programaOperativo_actividad_programaoperativo_id_193a8c36    INDEX     �   CREATE INDEX "programaOperativo_actividad_programaoperativo_id_193a8c36" ON public."programaOperativo_actividad" USING btree (programaoperativo_id);
 O   DROP INDEX public."programaOperativo_actividad_programaoperativo_id_193a8c36";
       public         postgres    false    225            =           1259    44316 ,   programaOperativo_actividad_user_id_2cf1050d    INDEX     {   CREATE INDEX "programaOperativo_actividad_user_id_2cf1050d" ON public."programaOperativo_actividad" USING btree (user_id);
 B   DROP INDEX public."programaOperativo_actividad_user_id_2cf1050d";
       public         postgres    false    225            6           1259    44280 ;   programaOperativo_programaoperativo_dependencia_id_6f329d6e    INDEX     �   CREATE INDEX "programaOperativo_programaoperativo_dependencia_id_6f329d6e" ON public."programaOperativo_programaoperativo" USING btree (dependencia_id);
 Q   DROP INDEX public."programaOperativo_programaoperativo_dependencia_id_6f329d6e";
       public         postgres    false    223            7           1259    44281 8   programaOperativo_programaoperativo_objetivo_id_92a6ddfd    INDEX     �   CREATE INDEX "programaOperativo_programaoperativo_objetivo_id_92a6ddfd" ON public."programaOperativo_programaoperativo" USING btree (objetivo_id);
 N   DROP INDEX public."programaOperativo_programaoperativo_objetivo_id_92a6ddfd";
       public         postgres    false    223            D           1259    44355 %   users_profile_dependencia_id_e45b54d1    INDEX     i   CREATE INDEX users_profile_dependencia_id_e45b54d1 ON public.users_profile USING btree (dependencia_id);
 9   DROP INDEX public.users_profile_dependencia_id_e45b54d1;
       public         postgres    false    230            Q           2606    44092 O   auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 y   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
       public       postgres    false    201    205    2827            P           2606    44087 P   auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 z   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
       public       postgres    false    203    205    2832            O           2606    44078 E   auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 o   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co;
       public       postgres    false    2822    201    199            S           2606    44107 D   auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 n   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id;
       public       postgres    false    2832    203    209            R           2606    44102 B   auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
       public       postgres    false    207    209    2840            U           2606    44121 S   auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 }   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
       public       postgres    false    201    211    2827            T           2606    44116 V   auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
       public       postgres    false    2840    211    207            Y           2606    44209 R   dependencia_departamento dependencia_departam_dependencia_id_8bce7a3e_fk_dependenc    FK CONSTRAINT     �   ALTER TABLE ONLY public.dependencia_departamento
    ADD CONSTRAINT dependencia_departam_dependencia_id_8bce7a3e_fk_dependenc FOREIGN KEY (dependencia_id) REFERENCES public.dependencia_dependencia(id) DEFERRABLE INITIALLY DEFERRED;
 |   ALTER TABLE ONLY public.dependencia_departamento DROP CONSTRAINT dependencia_departam_dependencia_id_8bce7a3e_fk_dependenc;
       public       postgres    false    2864    219    217            X           2606    44359 N   dependencia_dependencia dependencia_dependen_adscrita_id_3b7c8390_fk_dependenc    FK CONSTRAINT     �   ALTER TABLE ONLY public.dependencia_dependencia
    ADD CONSTRAINT dependencia_dependen_adscrita_id_3b7c8390_fk_dependenc FOREIGN KEY (adscrita_id) REFERENCES public.dependencia_raiz(id) DEFERRABLE INITIALLY DEFERRED;
 x   ALTER TABLE ONLY public.dependencia_dependencia DROP CONSTRAINT dependencia_dependen_adscrita_id_3b7c8390_fk_dependenc;
       public       postgres    false    217    215    2861            V           2606    44142 G   django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 q   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co;
       public       postgres    false    199    213    2822            W           2606    44147 B   django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id;
       public       postgres    false    2840    213    207            `           2606    44387 W   objetivo_objetivo_dependencia objetivo_objetivo_de_dependencia_id_c4bd31b7_fk_dependenc    FK CONSTRAINT     �   ALTER TABLE ONLY public.objetivo_objetivo_dependencia
    ADD CONSTRAINT objetivo_objetivo_de_dependencia_id_c4bd31b7_fk_dependenc FOREIGN KEY (dependencia_id) REFERENCES public.dependencia_dependencia(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.objetivo_objetivo_dependencia DROP CONSTRAINT objetivo_objetivo_de_dependencia_id_c4bd31b7_fk_dependenc;
       public       postgres    false    2864    217    232            a           2606    44392 T   objetivo_objetivo_dependencia objetivo_objetivo_de_objetivo_id_ce277155_fk_objetivo_    FK CONSTRAINT     �   ALTER TABLE ONLY public.objetivo_objetivo_dependencia
    ADD CONSTRAINT objetivo_objetivo_de_objetivo_id_ce277155_fk_objetivo_ FOREIGN KEY (objetivo_id) REFERENCES public.objetivo_objetivo(id) DEFERRABLE INITIALLY DEFERRED;
 ~   ALTER TABLE ONLY public.objetivo_objetivo_dependencia DROP CONSTRAINT objetivo_objetivo_de_objetivo_id_ce277155_fk_objetivo_;
       public       postgres    false    2869    232    221            \           2606    44305 [   programaOperativo_actividad programaOperativo_ac_programaoperativo_id_193a8c36_fk_programaO    FK CONSTRAINT     	  ALTER TABLE ONLY public."programaOperativo_actividad"
    ADD CONSTRAINT "programaOperativo_ac_programaoperativo_id_193a8c36_fk_programaO" FOREIGN KEY (programaoperativo_id) REFERENCES public."programaOperativo_programaoperativo"(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public."programaOperativo_actividad" DROP CONSTRAINT "programaOperativo_ac_programaoperativo_id_193a8c36_fk_programaO";
       public       postgres    false    2873    223    225            ]           2606    44310 X   programaOperativo_actividad programaOperativo_actividad_user_id_2cf1050d_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public."programaOperativo_actividad"
    ADD CONSTRAINT "programaOperativo_actividad_user_id_2cf1050d_fk_auth_user_id" FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public."programaOperativo_actividad" DROP CONSTRAINT "programaOperativo_actividad_user_id_2cf1050d_fk_auth_user_id";
       public       postgres    false    207    225    2840            Z           2606    44270 ]   programaOperativo_programaoperativo programaOperativo_pr_dependencia_id_6f329d6e_fk_dependenc    FK CONSTRAINT     �   ALTER TABLE ONLY public."programaOperativo_programaoperativo"
    ADD CONSTRAINT "programaOperativo_pr_dependencia_id_6f329d6e_fk_dependenc" FOREIGN KEY (dependencia_id) REFERENCES public.dependencia_dependencia(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public."programaOperativo_programaoperativo" DROP CONSTRAINT "programaOperativo_pr_dependencia_id_6f329d6e_fk_dependenc";
       public       postgres    false    223    2864    217            [           2606    44275 Z   programaOperativo_programaoperativo programaOperativo_pr_objetivo_id_92a6ddfd_fk_objetivo_    FK CONSTRAINT     �   ALTER TABLE ONLY public."programaOperativo_programaoperativo"
    ADD CONSTRAINT "programaOperativo_pr_objetivo_id_92a6ddfd_fk_objetivo_" FOREIGN KEY (objetivo_id) REFERENCES public.objetivo_objetivo(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public."programaOperativo_programaoperativo" DROP CONSTRAINT "programaOperativo_pr_objetivo_id_92a6ddfd_fk_objetivo_";
       public       postgres    false    223    2869    221            ^           2606    44345 @   users_profile users_profile_dependencia_id_e45b54d1_fk_dependenc    FK CONSTRAINT     �   ALTER TABLE ONLY public.users_profile
    ADD CONSTRAINT users_profile_dependencia_id_e45b54d1_fk_dependenc FOREIGN KEY (dependencia_id) REFERENCES public.dependencia_dependencia(id) DEFERRABLE INITIALLY DEFERRED;
 j   ALTER TABLE ONLY public.users_profile DROP CONSTRAINT users_profile_dependencia_id_e45b54d1_fk_dependenc;
       public       postgres    false    230    217    2864            _           2606    44350 <   users_profile users_profile_user_id_2112e78d_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.users_profile
    ADD CONSTRAINT users_profile_user_id_2112e78d_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 f   ALTER TABLE ONLY public.users_profile DROP CONSTRAINT users_profile_user_id_2112e78d_fk_auth_user_id;
       public       postgres    false    207    2840    230            �   -   x�3�.-H-R(-.M,���2�tL����,.)JL�/����� ��      �     x�ѹq�@C�ؿ�������aB	h�$��c?��tbg�;��Y��fvw���|��k3�a�1�KL�&�e�	������������������y��qy>�<��<��8��0B^�ߊAȋ$�E�	y1�����x��<��4R^:)/����$�e��Iy9�����|��:��2J^9%���W{��Eɫ���P��R�����л��ӡL:7�������A�r�_���)��gs�9���2y�����G��?��������>�p�m���?c6U      �   [  x�e�ێ�0������bNI��+U��TG�n�}��x<s��߈/�Ǚ~:��?�¼��g��O\�
����I�j��0�UR�@T���
f_Ѳ�c0U�I+�)B�ReCT�A�*l�I6H��f��?S���h�Y��.Z$�IP ����i��7���>L���DźFzhu�J+����;v�0�*�"����g��hڬL%뮅��YZ4�
k����P���ĳ���Ǐ?a����:/m�B (�eP�@�hɠ������V����1,_�`S�{:}��6:��O��IG]v^�q���ˮ���c�O��=��cT������|������|E����-����(�8���U����?�ֶV)����K�*�+A0'w��Ӗ���l�ۮ�`mk�Yš"�*�
EEB�S�"c���\�òq2��VlS�*��"��Y��E��]���HN�c��/����mT>	@=dT�A)dD� ��t}.a6.��ٶ*Cy���	H��Cއק]���qZ���~��qi�am/�V}�%�R�A%�l@G� rP⠬`N��?N3��UQ��r 8T�\'B (0������?=�K�      �   n  x�m�[n�@���U���Qg��D��Z	�z��@�pO]E7�il�&z������apt�=oӀb�H�\���4���ruXr\���cω[ۗ�%/&�-�/�^R�:��!��`cO�C��	Г�%!��Oz�1�c�x���4�n���H�C��ZU5I�0I=Χ�
�m!��Q�������b��e;��*�I)5��YHY���Ǫ��arQ�����n2���V]z�X
��ҌVO���������N���A-Mli�� �c��l�/�K��JZk-�K���V����YS����өa1ð����@d�"))7�9������i���iӨT*�R �U      �      x�3�4�4�2�B�=... %      �   �   x���q@!ѳ;��%��5�Ҝx��~�#b�4�i��fO7gz��˛>�|m!�2�@&�Ȉ
�Q#C�Ȕ2�����b�b��=({���(�^4a/6a/a/.a/i/i/E�˙�1I{Y��l�^n�^�^^�^>�^-�^��WA٫�ٷ���US�jS��P��R����z��Z���^'m���oh�^o�^�^_�^?������"?�      �      x������ � �      �   I  x��V�r�H����*'w	���!EI�T��mWN����b��ŲN��S:`�rv)~�z� !�UŲB��L�tOτ��0<�E�C���KeW����&�L�EBI0#k� ���fS�2�Yvj�Z���RKI�ƇSG�1㩎��C����(�^�=����I� ��:�iˮ�ɷ��������\&�o���#�S2�xIvk��O�ĸGŢT�؝<�5�؟dh�7�I�W"� ��ԡH*_̵����Υ~b3�.��Ħ�*n�ѥ�a���Lq�@H<�Kg|��]��B�}0�����<*��)�V]R��`�^'����i��T���QLdE��� �������w�^g���:��D8<h��dj�U? �KI� 2h�� �p�?������۽�_�4sn�^���(�\�M�ÂČ�g�F�G�7�=.q�q�tI��=3R�KvnWB!{ �1	nD���C6ܲw�ar�-6�x�.�u�~��y�v�p:Iq0�`�YxR�`[-�`�<���cuکF4<����Ucᛚo	/%�n�M	�E�[�t�V���xU��|	?�nt��ʹ��4˷��+�C�Bߡ��r�J����Aj�R�!�L`�נ;�|��i����@��v�I��'I
絙��	YJ�ܿK��B��c���t88H�I��
��(ڮ`��5՜_;aQ�@E'���:�\*�a"%W������a�{v;��j}�ͥ�{'�`��)W��"��[y�#4&șE]nM�(�jm�*w�[�mtV�b�� #�Fpî)]=�i8�[��E*P� {7�k�|��)|�d�ouʃ�|g@U����M��Ġ(xq�����kJ*�X�n�0b��ǫb�_!�/+���_p)@ŕ˟�N��ID�+�
���'�X2�x4�2�LOw��+���OdL�ň2�QAzcB��D���T�SI_��7D��A�R��a/�v�V��s�O��]^T��%���D�q&k�]��U���×B���uӪ��A���nW���l~�>u*��%��v�k{O/|c��d�y�= l*ɷ�����hg՞�.�8*���
z�IQ�ԛ��}�30�����������'>��R~��;��A�G�5M/�!�fT��!cg�~�j�hq6�v �Yg���*少r僀�;����v�+@�VE�?U�=��`��c�#$��n��V3��@V�z�-l��=�c9�6<98��BR59ګ�8��u���Z|����Յ������m��g�co,�:��u��=� sɾɥ�'���;ϧ�(]h���;ݪӟZ'''� g�      �   �   x��1
�@ �Wl��&�GZIPH�`ks�,�p�®'�.����I;�L+���/�2iH8^�_��~8�^�iH����ԗĲ�=�<��Tem4d������㡪<t����(˶-�<������pt��s�u/`      �   �  x��[ˎ��]�_A�Z!���n`;���op�M�p$΄��� F���2�������[��F�&%�da�֩��:}��������J�Z2��<�PN�C"!"�Pw�r��4��m]��ǼJ�EZ�鿷OE�ٮ͏׿5EB�_�$,�oȁ]�Dh�u��@��8Ax�S���]�>���I7��}��Un��~��-����2���,�u���j]<���We~��?�$`����0�98���-ҷMӮ�:_���ԇ��i�M�r�|*��&�@6H����#���nS<�����y�|�*�������}��w�c�n��M�`b�	�-��^�o��m�ٶy)G V.j�仲���_oWn�z�*4���g�,�Me�r{�MN2`�)����'/�O��Ql��L`.46�h���o�tg1���R�P�ѡ|/�����U�jf�F�O��A)JN��_���Q�;ۄji�C����.�*���e3B��#���h79�Y�w��n���f�2��䰅�G*9�7{�/�� 3,ry)L^Fq~*�3xG����B�l�o����<?x(Ŕ�=��W�?uѺ0~*�-���O-�?���]���?�����[u��TB"*q�	���F�1�d�C��-��.y��u	�M]t6�~YPPa|IH8-	͸�H;)�����U� �!oK���k�R����$��M�ط�&o76����y���	y�wGpnӘ�K�yWty�6Uդ�H�
>����	�wB!j����Ĩz !E�h�w�K��)�@�E�MB�d*2E,�#f8m&bOgR	 2.�&�&p�g�q�m	]���˷�3���Đ���Hi$����x�wHgYc�2��|F*��ɒ��2ͱ:A|O^����)�-�w�{x�km責7�������g��Pc��*��ʑ��yL�=�ȹ�g����)R��OJ�0^U �F���!I#�� �R8�A�Oa�cR���Gp��q��-��:���*��x!�K}
dl{#&�F�l�.��_@b�Q:o�%ᙤ�+���\|_֎��Ԋs��dh*k�
�nՖ������/PGs|���/)�d���{{�C�J����Z�V���(��$��V�A�^��h"��h����s\K�%#��i��7�H3������y�ռ��c$�RL:Yz�N`Y4RH[�x�sv<�#qG�$P��D���M��s�2�ԙ��`�%�hGV80��W�WH�r9=Ђ� 7�c��&�����'�6���v�3Y�lD-	��SK.�T��|�ƦG7$:���R�.��8�"	"Ն�~�Q��o+���j�[�ZU��9���ݼ#�a�V�����*��j9%���Q5r�(�S��><�?~K�c2dS�&r����A2����M��T�O�ܦۍo�XHU=���m/�v~F�(Zr�!��~����ۮ�^a��C�2�L��E�M��_k��C>�R��8�w
���ږ�#/iR�ǔ���/���g��z���������H��%�(E[�)����ˎs1�T\�c=��M��8���!�Q�d��'5b���J8_�y': ���"���9��ӋQ��G�l���j=���w�ER`�+�i!_��:� "���Ye�2��ai7m���Џv�GK���ؠ�-���D��Tnv1��"�%�S[`K��@���橬�٭���M
���n)R[u2#:�2sqF1�ĥ�J&:1K���K��P�nX�t?�f7��C�����R��#LD��!�f�_�|A�ʈk�k�Gl�Ҙ�V�2bW���+1v��=2b\�$:C��$��iF�����:
?|.s����rs�4���Y�4^-a"���R�2���48�7�TF�����������Ɉ'�����N�m�d�}ζ�~� �i��8";�)u�5\��y(#؍ s5�4P�:�7��-��'W�B1�PB�����Ka�b8\��R���cW�Ҝ�C��~�� E_Y2��+�	���C]7O�����h��J�9��1",$Wv '�(��|ذyIu�"�7?R���`0P����q�ϔ���mH׳q�ŕ9Y_>��`C{lb�%U�"L�m"z��Gw;�j���3ԷR1���nV#��5�i`��4����!��F��d�O��.ҋG$X1w��S��z�|�Q�2�B;͕1���dA�ذ�x�տZr��Q�fH�ί��~�<��qc�%D��
O�����@G�QwW�_�9�g�iSc3��B���]̺m�a�{@���
�a2���]:���hiho�"�/tX�= s���ʧ���tH	=�`�(�K�h�"1
I��Xս@!�#|�40
I�GԾG-2�8GP`2��$ȿ�AG�JV�B��Q!{-,(�saGN}�#D"[� ��Řr���*ܵ�<�~.}ć�-&�iq��N�ya [�1�b4�3D�+6y�g.R����S	O�Z�f����!�0b^p���OM>m�6�v[�~�|�v �&�PH��']L������CYC�[�v�PHL.�8���C��-<(���s��a�3e�E	c��)%NVU��K�+�n��ëEz����m�}���]��x�H�~e�Y�W�msWV����k�ژ?�^\Yǩu<����Hh���c�-n�܄(���=3��!�pd�EZP��f��.�����~�6���^L��9�G/:m$/*Z�]tΤx ۔5!�k��
w��;��{m�� A�2!�d����XO�~e:�/\@P���N%�"PA����s�Cud������![2%)s/���=�|@��I���+��$��������},f�ݘ��X*��^���0��z9��~/I���͛7�JL|      �   �   x�m�K�0Dמ� -�Sp6�1%���$E*�'-*?��g��hC}��ˇz�j�AϮ��J'ފ�S`wG�>4���ĭ��ؐ����M_�7���i$�z�1A��C����Lt&����*g��,�m�<5Z�a�1�}��۶.F�f�Duо�Y?��	0U�S���N⧁))��B�� ��vK      �   �  x���m��0��S����w.�T���ͺ�@V��wl	ūD���yϼ3c��Ե�o����� �P�0W@�y#��T�<
(�$��7"P����L�J¤44*X�&��%�2�d��lݝ1��j�t�����uU�g04m+�vg�κ��־��lO]8�Y��!���.�E�,ظb[��<J�?���Փl�&�c)�m�l��3~�E)��[y�+�-�ˈ߸P?�P�E�Y)��)����� �&{(Y�Q�q����R�TH�P�R$������仍�}��o	r�O�����P���T}?�`?���M��3��8�u���&�H|%��G/�$�I(qCQ���Cw�_�(���C��G������Б����3C��}[����g�����E�����g��{~��ld0�QCՖ��Y'J2�0�!�=!�c���B�-	|O�ycI(������v����iT���;;$1Y�`\-��<j�y_��R�aQ�~i���C����E��4�)s	v}�K]�m������S �$�|껂j0Y%X�9�m[
{�g��2�eJ"��f`�Ɣ�(���hL"lS��ǩ����ڏ��ȑa>��	�/l�d��Щ�P{;�����)��Q��<� 6AJ      �     x����n�0�s�}�F�"�a[RdT%bCl�%1�&����I�ڽ��Rɧ�_��o��k�_Q;���^�ws���o�����	�p"����'��"#��XZ�S,s�X�����ٰ豖����8�M��ͪݠ���d�͗UZсV�j��"��b�Մ���I��к�d|�;[�/����j���]l�`�D~��H����"�v��.���d��{=��j�`y�IҌ]g]�,�u��(�2KQ�"nef�4O^����B��^� ���{�]��B|�Nv�C��ڶ'�V)�����c�ɱ�j�e��zs��l�CэN�wt2���d/��]��r^�m����DsL 3?�����Ƶ��t6�Ñ��ݡߟ˳�|�}ڡ{��������?U��0l�`ՙn�������I��?�nkˢr�7��b�/�-�)�E�Rȳ������vPd��H]����,1�6�;�D� i,\��,Ͼ_��y�����$s��>}���~N'��#��      �      x��[=�#Ǒ�{~E;AF�F3��y�咷�qC��%��(`j��ժ��	k��k���b=��'�%�^fUu50�EȒd�� �UY�/3_f�T7�ի�ԘƝ>w��^�nn=�P��5��?�������>�[7�u�Y�>��?�P�އq�������6�uo��G�1^��p]����`��l3��b��7~�Ɵ����}ov����\���s�Z,�F�;��%�m|w��w��v?�'�7�δ�mN�Q��a���LV�dm;�u��x�]�po�N���1)E���띿�n��V7O��,Ub��7IIP�i�G����ip��6��la�ޯۤ��~q��VD�:�#4�z�M�
��i���.��Bhy̶X�A[{ۍ���Fk�Z;����A��ކ���9N*Y�o����#4����y�.>��u���:��y
���Ӷ6�oO���X���ؐF���`��`�`����K!�0��Q54#-�8��<��Yփ�������..MݎA�찪'��_�-��틗?����^}�5�j_�~�/�	Ǧ|�����
��Yu��}0ݰ�aoh�q�_=7����y���v8��P�H�4S;N>D=�~p"u4��FG�����6�������gd]W߉a�P�+�P�~j�x�������&X��!Y��1�AF��n���D9�ֆ �M�rR���}P�7�t-�B�����!�B�`����t�߬$*�n��� ����ӫ��ͳ�'U$���N��$Y��������W�41�!�y�:l׸|�����$[)�����p4��3�rj�r61��\�Z�Cе�4L� Y
�o�j�q��udx��M�C�-i�[�I�����1a$q���gA�x�x �%ir/6�ML��'>�> �����)ǧt�uD,ZG>5��ag:���~�u�NMs)�����լ>�k&��9�#�7;j}o�}�	��&�V}m�~K��N�G��O��~I3\���[�6�>iX�gܚ=���Ӈ�>Lm��%#��3��j8(�<�q{G�1 }�"��M�I`��Ӈ��T��Q�Xj7����Ѓd��d��Xc��8�%��@��VQ8h�X��"+ZXTq<N��&a
����|r�c���@J&��u��b6�����*�j��Ac�j��;�6�d�),�v�9Ify�����z��{]W?
V������+^B_�D�=#�{�0C���x��ܛ�ʳ��Q��=9��vo�8�B%�����|Q3��̅��?}�04��;��B�d��c�K��.(�fa����Χ��T�.0S����O�]�5�^G�$�d�m�TH�77�qN�E�@e��Vb���0����E@��n����p�]�z-%j��p�:��buŠ }��A��Hj����=�B�&-�ԉL�ވu���JHD�KE���%ǘ/,E�e)̨H�no���*2�T�u�����V5�n7�6VJ˚�(rK;���*��O�1�Z�ը͕PC����1� l���*Ha�oQ�!����J�}��{�_�:���pC���2Z���S�	������W�#~�R�8��#	����	�}h9<=H:h&����үA�C��6��%7�ΰ�Mʚ9�)�h#���o50�����Y���HG�Q'F$�(�,O��o�7�yP13s~�;����ʕA�SR�rј~�d�[�"A�����q�`&���v
�&�N��w�T�n��$�8	l��٩�4c9#$��I\���aO)VΌ-��E�VC�V��9@7<P\5���88�ɶ�4'J��4�JA?Ĵ�{�8�����^X�Z��Z���&��~�_�W騥G���T]6�y�"Ff�%�|uG+��,mw�ܣ��ȶ�`>����z�q"�f�}6Ԕ�O��o�< �ྀ��� 
p�%q�왜�̚�		�j;}�z���o��{��l����`,�\2�D8�&v����1�+)�NEa���IS	�i�b���m��1�J�L���M�ڶ�P1�\ϕ��H5�'��j=��a�}l�	T~!ɐ�&�I��7Yi��,t�H@�[�	#����'Uv$��= �'�q��b�J�>���N�x��Ėk�U��h��"j!�[a��7EN0Q�}��pw���XJܐ����7�A'^(K�*�,��3]T}�ckV+��J��H�4T� >4�i�{M�'K�h"��`���q�i��L���P�JbI��eɰ���!3WzU���l%Q�`��D����VP�|�l�UEK�4���Wk[�&o��Ō�u�$�DCL�<Х�~���+pQ7)1�xdi��"�˝�p[Du�`)@���j�mscƔ���a�S)���ɔ�]`l�U���S�rTP�f*�`�j�����gB�#E�6U@��w!@b'0%��|���u������},vs�>����ԍ	���=��Aڌ�_����>f�������E ��^�A��+s{u�|]}�rsD�����$C�4ēn�v;l��8�
���kv��w�r.=�cxR˒s?�����od����%M�%,�mwR��U
�MяZ�T�������\��/����eSԍ���N�²L+0WK\�l��#��h�L����T���ۀ��^KXe�Lt�Wd�E�Q���sG�7j�5l<�yGm�FJ7[��,۝04��2�+G~e��E�#D�"ɡ�e��*C�hq�cqp=d:�x)��W��yG��s/s�<ֱ��g~6-��Y@$��Ve�]!��]���E��,ˣ��^���N-A��b$ݒ9`;�b?+�Q+�iX�i!7k>T��Js�1/�H� 8Љ���Z���ʓ6��{�x8wlԊ��L��[�,��U-Ӈ��������XrXa��;k�"�I��ճ�ۯ�uz��EXg�H�����/G3��߉�idV�9�4����c���2 7�YL�.�؍�S�]�VxLdG��]����,����~�)�r�/(0� ��Z�1� ڊ]`��O���jAG
d��#Iid1b�i�o*�I?�Cd���?Ph�lI��1���R�@?�]����k��<;-�GK�eM��e��U���a1@�2���{�8��F���7��׉�a�Y%�T%oN�ś�?�{��ꬁ�\�"�h�A�jXJ}����/U�Q!�`Wv4�l�=굀ػ.e���d8���4U\[e:!���`���q�Ca�C�ٶKC^^up�b�4�3Ҵ5z��9����AٞЋ�pn̾7$1JU�[b����l��V��Y�� ڷe����r�����M����2�z���;o��N�r'�Q/izc"!'�%��ztYCQr \���Q�uQ�_�/�2���@I�Ro��!�E�Z'��A<|�X��c��|�j��,ާ<��ɴ*E:f�CJ8�{ ��ܺC(R��ѿ)�+/c�?K}i\���R%�I����5ӕ�A�*$ƔЊ��47���.�I�%�T�PNM��Ǧˍ<�<��}=��!�GjLD�d�='��}b7>O$�I�R��g��
zˋlǅ:I�j}׊�~��9��~k����zX}�wQS羻��d��)�9�P?L��YO�����Χ�l�i͛Zpz��'�x�b�x���c�F&D��N��!mUO��I���$:��v��wm�^�+-;�а)�����<�̩�0���y>T+���y�~�--�U��T�g�,�T�	��ϣ�oވU��Uٝ��ӂ��W?7;31<ki�(h��K�Z$�DX�΍��&�Xc����l��<��'O+TT?.�,�[�˄�g˘����"��|��y ��H��L��N��hA���rh�lm�rx�`�8���H@��R���Rՙ�7tV��g�����U�Q���R��Nwjn���ԥ���+I10�����c�^L�*��x��Z��|?#���0IS�g�Lc�F/HM]�}����E7w���a4�+m��B�$%t�*�e���:��M�
G�YِlM��,2�g0��i;���@�*�����jO2�7�T� K  o�3��\���}A��|��,ԣM]݆e흘���m��[��JV���Q�vL���7}�x'�s^��M���FD����?�TC�Y�/�k�A2���N�@+#�Ao�&OM�>4��
�ӛe]�{&���j�+�}hXi���f�0�ݜ�x,^Ja�2�5��2~яzl&�ʵ:s����aJ�ê��A�������
�։J�����4Q���m=�{��t�Ζ���t�Ӆ�ӛ:>'"gǌM��M���h�p�EK<2�.GWgt<�Wg5��H�a.���U�
�#$�@˓�
�G.�_�bp/mUO��p}uu�����      �   7  x��˕�0C�V1s��^^�u��&�Q��v��1�KW���GWI�+sN�䝔�wJ���aNإp���ê����Dk*���ڏ���<�QX���ɾR�!e���M�X�t��Y���^��\u�3n�p]`��'3qC����4J��^�'�&�u�4��eR.	p���`��"Rʑ��-���C���O��o}C�*�5}a�},M�T���X����@���wZ:"9��ѭ�u�s٢Q�pQ��O�NP#�T��\����U�B�caй��%�Au/p�,p�[�&��l2�l6���l27���F=c�      �   _   x�E�A
� E��)��(�����a�4������.�V���&+8mqC-��3���%'v��w�~�d��8Jm�],�s
Y��f�17dw�      �   8   x�3�,(*MMJT02�Ӌs�R�K2��RR Ҝ�Pux)cN#�=... �-      �      x������ � �      �   _   x�}��� �7�"�·1�Z��E⽫��>���3-븈icj3o-��Q-��`�d��_]���".������+����e��EDޱ)�     