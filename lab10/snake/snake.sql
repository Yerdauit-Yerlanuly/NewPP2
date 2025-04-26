--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-04-05 20:40:17

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 16390)
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."users" (
    id integer NOT NULL,
    name character varying(30) NOT NULL,
    level integer,
    speed integer,
    apples integer,
    mode character varying
);


ALTER TABLE public."users" OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16389)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 4907 (class 0 OID 0)
-- Dependencies: 217
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."users".id;


--
-- TOC entry 220 (class 1259 OID 16404)
-- Name: user_score; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_score (
    id integer NOT NULL,
    name character varying(30) NOT NULL,
    score integer
);


ALTER TABLE public.user_score OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16403)
-- Name: user_score_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_score_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_score_id_seq OWNER TO postgres;

--
-- TOC entry 4908 (class 0 OID 0)
-- Dependencies: 219
-- Name: user_score_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_score_id_seq OWNED BY public.user_score.id;


--
-- TOC entry 4747 (class 2604 OID 16410)
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- TOC entry 4748 (class 2604 OID 16411)
-- Name: user_score id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_score ALTER COLUMN id SET DEFAULT nextval('public.user_score_id_seq'::regclass);


--
-- TOC entry 4899 (class 0 OID 16390)
-- Dependencies: 218
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, name, level, speed, apples, mode) FROM stdin;
9	Akylbek	10	14	11	finished
10	Qwerty	3	7	2	finished
11	ds	3	7	4	finished
\.


--
-- TOC entry 4901 (class 0 OID 16404)
-- Dependencies: 220
-- Data for Name: user_score; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_score (id, name, score) FROM stdin;
4	Akylbek	25
5	Qwerty	6
6	ds	6
\.


--
-- TOC entry 4909 (class 0 OID 0)
-- Dependencies: 217
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 11, true);


--
-- TOC entry 4910 (class 0 OID 0)
-- Dependencies: 219
-- Name: user_score_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_score_id_seq', 6, true);


--
-- TOC entry 4750 (class 2606 OID 16395)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 4752 (class 2606 OID 16409)
-- Name: user_score user_score_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_score
    ADD CONSTRAINT user_score_pkey PRIMARY KEY (id);


-- Completed on 2025-04-05 20:40:17

--
-- PostgreSQL database dump complete
--

