PGDMP         $        
    	    {            new_exchange    15.2    15.2 G    X           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            Y           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            Z           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            [           1262    64445    new_exchange    DATABASE     �   CREATE DATABASE new_exchange WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE new_exchange;
                postgres    false            `           1247    64488    bankingtype    TYPE     a   CREATE TYPE public.bankingtype AS ENUM (
    'CryptoWallet',
    'BankingCard',
    'Ewallet'
);
    DROP TYPE public.bankingtype;
       public          postgres    false            T           1247    64452 
   cryptotype    TYPE     D   CREATE TYPE public.cryptotype AS ENUM (
    'Crypto',
    'Fiat'
);
    DROP TYPE public.cryptotype;
       public          postgres    false            f           1247    64519    mark    TYPE     |   CREATE TYPE public.mark AS ENUM (
    'one_star',
    'two_stars',
    'three_stars',
    'four_stars',
    'five_stars'
);
    DROP TYPE public.mark;
       public          postgres    false            Z           1247    64471    role    TYPE     N   CREATE TYPE public.role AS ENUM (
    'User',
    'Moderator',
    'Admin'
);
    DROP TYPE public.role;
       public          postgres    false            o           1247    64560    status    TYPE     �   CREATE TYPE public.status AS ENUM (
    'Pending',
    'Timeout',
    'Canceled',
    'Inprocces',
    'Approved',
    'Completed'
);
    DROP TYPE public.status;
       public          postgres    false            �            1259    64446    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap    postgres    false            �            1259    64458    currency    TABLE     0  CREATE TABLE public.currency (
    id bigint NOT NULL,
    tikker text NOT NULL,
    type public.cryptotype NOT NULL,
    name text NOT NULL,
    gas numeric NOT NULL,
    service_margin numeric NOT NULL,
    reserve numeric NOT NULL,
    max numeric NOT NULL,
    min numeric NOT NULL,
    icon text
);
    DROP TABLE public.currency;
       public         heap    postgres    false    852            �            1259    64457    currency_id_seq    SEQUENCE     x   CREATE SEQUENCE public.currency_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.currency_id_seq;
       public          postgres    false    216            \           0    0    currency_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.currency_id_seq OWNED BY public.currency.id;
          public          postgres    false    215            �            1259    64574    order    TABLE     �  CREATE TABLE public."order" (
    id bigint NOT NULL,
    user_email character varying(320) NOT NULL,
    user_cookie text NOT NULL,
    user_buy_sum numeric NOT NULL,
    buy_currency_tikker text NOT NULL,
    buy_payment_option bigint NOT NULL,
    user_sell_sum numeric NOT NULL,
    sell_currency_tikker text NOT NULL,
    sell_payment_option bigint NOT NULL,
    date timestamp without time zone NOT NULL,
    status public.status NOT NULL,
    service_sell_po_id bigint,
    service_buy_po_id bigint
);
    DROP TABLE public."order";
       public         heap    postgres    false    879            �            1259    64573    order_id_seq    SEQUENCE     u   CREATE SEQUENCE public.order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.order_id_seq;
       public          postgres    false    226            ]           0    0    order_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.order_id_seq OWNED BY public."order".id;
          public          postgres    false    225            �            1259    64496    payment_option    TABLE     &  CREATE TABLE public.payment_option (
    id bigint NOT NULL,
    banking_type public.bankingtype NOT NULL,
    currency_tikker text NOT NULL,
    number text NOT NULL,
    holder text NOT NULL,
    is_verified boolean NOT NULL,
    image text,
    user_email character varying(320) NOT NULL
);
 "   DROP TABLE public.payment_option;
       public         heap    postgres    false    864            �            1259    64495    payment_option_id_seq    SEQUENCE     ~   CREATE SEQUENCE public.payment_option_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.payment_option_id_seq;
       public          postgres    false    220            ^           0    0    payment_option_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.payment_option_id_seq OWNED BY public.payment_option.id;
          public          postgres    false    219            �            1259    64530    review    TABLE     �   CREATE TABLE public.review (
    id bigint NOT NULL,
    user_email character varying(320) NOT NULL,
    text text NOT NULL,
    data timestamp without time zone NOT NULL,
    rating public.mark NOT NULL
);
    DROP TABLE public.review;
       public         heap    postgres    false    870            �            1259    64529    review_id_seq    SEQUENCE     v   CREATE SEQUENCE public.review_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.review_id_seq;
       public          postgres    false    222            _           0    0    review_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.review_id_seq OWNED BY public.review.id;
          public          postgres    false    221            �            1259    64544    service_payment_option    TABLE     �   CREATE TABLE public.service_payment_option (
    id bigint NOT NULL,
    banking_type public.bankingtype NOT NULL,
    number text NOT NULL,
    holder text NOT NULL,
    currency_id bigint NOT NULL
);
 *   DROP TABLE public.service_payment_option;
       public         heap    postgres    false    864            �            1259    64543    service_payment_option_id_seq    SEQUENCE     �   CREATE SEQUENCE public.service_payment_option_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.service_payment_option_id_seq;
       public          postgres    false    224            `           0    0    service_payment_option_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.service_payment_option_id_seq OWNED BY public.service_payment_option.id;
          public          postgres    false    223            �            1259    64478    user    TABLE     �  CREATE TABLE public."user" (
    id bigint NOT NULL,
    email character varying(320) NOT NULL,
    first_name text,
    second_name text,
    hashed_password character varying(1024),
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    is_verified boolean NOT NULL,
    registered_on timestamp without time zone NOT NULL,
    buy_volume numeric,
    role public.role NOT NULL
);
    DROP TABLE public."user";
       public         heap    postgres    false    858            �            1259    64477    user_id_seq    SEQUENCE     t   CREATE SEQUENCE public.user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.user_id_seq;
       public          postgres    false    218            a           0    0    user_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;
          public          postgres    false    217            �           2604    64461    currency id    DEFAULT     j   ALTER TABLE ONLY public.currency ALTER COLUMN id SET DEFAULT nextval('public.currency_id_seq'::regclass);
 :   ALTER TABLE public.currency ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    216    216            �           2604    64577    order id    DEFAULT     f   ALTER TABLE ONLY public."order" ALTER COLUMN id SET DEFAULT nextval('public.order_id_seq'::regclass);
 9   ALTER TABLE public."order" ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    225    226    226            �           2604    64499    payment_option id    DEFAULT     v   ALTER TABLE ONLY public.payment_option ALTER COLUMN id SET DEFAULT nextval('public.payment_option_id_seq'::regclass);
 @   ALTER TABLE public.payment_option ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    219    220    220            �           2604    64533 	   review id    DEFAULT     f   ALTER TABLE ONLY public.review ALTER COLUMN id SET DEFAULT nextval('public.review_id_seq'::regclass);
 8   ALTER TABLE public.review ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    222    221    222            �           2604    64547    service_payment_option id    DEFAULT     �   ALTER TABLE ONLY public.service_payment_option ALTER COLUMN id SET DEFAULT nextval('public.service_payment_option_id_seq'::regclass);
 H   ALTER TABLE public.service_payment_option ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    224    223    224            �           2604    64481    user id    DEFAULT     d   ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);
 8   ALTER TABLE public."user" ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    217    218            I          0    64446    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public          postgres    false    214   EX       K          0    64458    currency 
   TABLE DATA           h   COPY public.currency (id, tikker, type, name, gas, service_margin, reserve, max, min, icon) FROM stdin;
    public          postgres    false    216   oX       U          0    64574    order 
   TABLE DATA           �   COPY public."order" (id, user_email, user_cookie, user_buy_sum, buy_currency_tikker, buy_payment_option, user_sell_sum, sell_currency_tikker, sell_payment_option, date, status, service_sell_po_id, service_buy_po_id) FROM stdin;
    public          postgres    false    226   �X       O          0    64496    payment_option 
   TABLE DATA           {   COPY public.payment_option (id, banking_type, currency_tikker, number, holder, is_verified, image, user_email) FROM stdin;
    public          postgres    false    220   �Y       Q          0    64530    review 
   TABLE DATA           D   COPY public.review (id, user_email, text, data, rating) FROM stdin;
    public          postgres    false    222   @Z       S          0    64544    service_payment_option 
   TABLE DATA           _   COPY public.service_payment_option (id, banking_type, number, holder, currency_id) FROM stdin;
    public          postgres    false    224   ]Z       M          0    64478    user 
   TABLE DATA           �   COPY public."user" (id, email, first_name, second_name, hashed_password, is_active, is_superuser, is_verified, registered_on, buy_volume, role) FROM stdin;
    public          postgres    false    218   zZ       b           0    0    currency_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.currency_id_seq', 2, true);
          public          postgres    false    215            c           0    0    order_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.order_id_seq', 7, true);
          public          postgres    false    225            d           0    0    payment_option_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.payment_option_id_seq', 28, true);
          public          postgres    false    219            e           0    0    review_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.review_id_seq', 1, false);
          public          postgres    false    221            f           0    0    service_payment_option_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.service_payment_option_id_seq', 2, true);
          public          postgres    false    223            g           0    0    user_id_seq    SEQUENCE SET     9   SELECT pg_catalog.setval('public.user_id_seq', 2, true);
          public          postgres    false    217            �           2606    64450 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public            postgres    false    214            �           2606    64467    currency currency_name_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.currency
    ADD CONSTRAINT currency_name_key UNIQUE (name);
 D   ALTER TABLE ONLY public.currency DROP CONSTRAINT currency_name_key;
       public            postgres    false    216            �           2606    64465    currency currency_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.currency
    ADD CONSTRAINT currency_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.currency DROP CONSTRAINT currency_pkey;
       public            postgres    false    216            �           2606    64469    currency currency_tikker_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.currency
    ADD CONSTRAINT currency_tikker_key UNIQUE (tikker);
 F   ALTER TABLE ONLY public.currency DROP CONSTRAINT currency_tikker_key;
       public            postgres    false    216            �           2606    64581    order order_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public."order" DROP CONSTRAINT order_pkey;
       public            postgres    false    226            �           2606    64505 '   payment_option payment_option_image_key 
   CONSTRAINT     c   ALTER TABLE ONLY public.payment_option
    ADD CONSTRAINT payment_option_image_key UNIQUE (image);
 Q   ALTER TABLE ONLY public.payment_option DROP CONSTRAINT payment_option_image_key;
       public            postgres    false    220            �           2606    64507 (   payment_option payment_option_number_key 
   CONSTRAINT     e   ALTER TABLE ONLY public.payment_option
    ADD CONSTRAINT payment_option_number_key UNIQUE (number);
 R   ALTER TABLE ONLY public.payment_option DROP CONSTRAINT payment_option_number_key;
       public            postgres    false    220            �           2606    64503 "   payment_option payment_option_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.payment_option
    ADD CONSTRAINT payment_option_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.payment_option DROP CONSTRAINT payment_option_pkey;
       public            postgres    false    220            �           2606    64537    review review_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.review
    ADD CONSTRAINT review_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.review DROP CONSTRAINT review_pkey;
       public            postgres    false    222            �           2606    64553 8   service_payment_option service_payment_option_number_key 
   CONSTRAINT     u   ALTER TABLE ONLY public.service_payment_option
    ADD CONSTRAINT service_payment_option_number_key UNIQUE (number);
 b   ALTER TABLE ONLY public.service_payment_option DROP CONSTRAINT service_payment_option_number_key;
       public            postgres    false    224            �           2606    64551 2   service_payment_option service_payment_option_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.service_payment_option
    ADD CONSTRAINT service_payment_option_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.service_payment_option DROP CONSTRAINT service_payment_option_pkey;
       public            postgres    false    224            �           2606    64485    user user_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id, email);
 :   ALTER TABLE ONLY public."user" DROP CONSTRAINT user_pkey;
       public            postgres    false    218    218            �           1259    64486    ix_user_email    INDEX     H   CREATE UNIQUE INDEX ix_user_email ON public."user" USING btree (email);
 !   DROP INDEX public.ix_user_email;
       public            postgres    false    218            �           2606    64582 $   order order_buy_currency_tikker_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_buy_currency_tikker_fkey FOREIGN KEY (buy_currency_tikker) REFERENCES public.currency(tikker);
 P   ALTER TABLE ONLY public."order" DROP CONSTRAINT order_buy_currency_tikker_fkey;
       public          postgres    false    226    216    3230            �           2606    64587 #   order order_buy_payment_option_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_buy_payment_option_fkey FOREIGN KEY (buy_payment_option) REFERENCES public.payment_option(id);
 O   ALTER TABLE ONLY public."order" DROP CONSTRAINT order_buy_payment_option_fkey;
       public          postgres    false    226    220    3239            �           2606    64592 %   order order_sell_currency_tikker_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_sell_currency_tikker_fkey FOREIGN KEY (sell_currency_tikker) REFERENCES public.currency(tikker);
 Q   ALTER TABLE ONLY public."order" DROP CONSTRAINT order_sell_currency_tikker_fkey;
       public          postgres    false    3230    216    226            �           2606    64597 $   order order_sell_payment_option_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_sell_payment_option_fkey FOREIGN KEY (sell_payment_option) REFERENCES public.payment_option(id);
 P   ALTER TABLE ONLY public."order" DROP CONSTRAINT order_sell_payment_option_fkey;
       public          postgres    false    226    220    3239            �           2606    64602 "   order order_service_buy_po_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_service_buy_po_id_fkey FOREIGN KEY (service_buy_po_id) REFERENCES public.service_payment_option(id);
 N   ALTER TABLE ONLY public."order" DROP CONSTRAINT order_service_buy_po_id_fkey;
       public          postgres    false    226    3245    224            �           2606    64607 #   order order_service_sell_po_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_service_sell_po_id_fkey FOREIGN KEY (service_sell_po_id) REFERENCES public.service_payment_option(id);
 O   ALTER TABLE ONLY public."order" DROP CONSTRAINT order_service_sell_po_id_fkey;
       public          postgres    false    224    226    3245            �           2606    64612    order order_user_email_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_user_email_fkey FOREIGN KEY (user_email) REFERENCES public."user"(email);
 G   ALTER TABLE ONLY public."order" DROP CONSTRAINT order_user_email_fkey;
       public          postgres    false    226    218    3231            �           2606    64508 2   payment_option payment_option_currency_tikker_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.payment_option
    ADD CONSTRAINT payment_option_currency_tikker_fkey FOREIGN KEY (currency_tikker) REFERENCES public.currency(tikker);
 \   ALTER TABLE ONLY public.payment_option DROP CONSTRAINT payment_option_currency_tikker_fkey;
       public          postgres    false    216    3230    220            �           2606    64513 -   payment_option payment_option_user_email_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.payment_option
    ADD CONSTRAINT payment_option_user_email_fkey FOREIGN KEY (user_email) REFERENCES public."user"(email);
 W   ALTER TABLE ONLY public.payment_option DROP CONSTRAINT payment_option_user_email_fkey;
       public          postgres    false    218    220    3231            �           2606    64538    review review_user_email_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.review
    ADD CONSTRAINT review_user_email_fkey FOREIGN KEY (user_email) REFERENCES public."user"(email);
 G   ALTER TABLE ONLY public.review DROP CONSTRAINT review_user_email_fkey;
       public          postgres    false    218    222    3231            �           2606    64617 >   service_payment_option service_payment_option_currency_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.service_payment_option
    ADD CONSTRAINT service_payment_option_currency_id_fkey FOREIGN KEY (currency_id) REFERENCES public.currency(id);
 h   ALTER TABLE ONLY public.service_payment_option DROP CONSTRAINT service_payment_option_currency_id_fkey;
       public          postgres    false    3228    224    216            I      x�K�0J355M51JN����� ,�      K   M   x�3��	q�t.�,(����,IM����446�4�440 c=C�?.#ΠP'N���ΠҤ�T�*�BR���� "�b      U   �   x�mͻ
�@��z�)�fo��T^Z���d/�`H�§ww��!��1�eu�뭎� �Q�Ą65Mt}�L�)�d@����V�Z;z�(��FIHM%mk��\�i��KN��K�����DIkt�Oh,���4YG�߲/��u�%��,���%�*�+w��	��=�      O   �   x��α�0����)�*mq37�`4.,�\"$�����UH�瓓OHH���ef(�rK!������1�١_x:�'���PW6�,�VU�*,�	z� ����ZS7��Z&d�ҏ��4�p�f�|�0.���ډ^a��k<i
m��J�㽖[�d������-�h!      Q      x������ � �      S      x������ � �      M   �   x�3�LM*�*M-sH�M���K���t-KOͫ�t�s�%�����ꙇ���$%��G��Y���T�{�df���V���g��D喧&U����s���������������������g��cJnfW� ��(A     