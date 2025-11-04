--
-- PostgreSQL database dump
--

\restrict eChgyH9isuHeYMd4naDpgj6avArun2IDqZC5J11EeoVNZo3asgry3jfFfK4TUWZ

-- Dumped from database version 14.19 (Homebrew)
-- Dumped by pg_dump version 14.19 (Homebrew)

-- Started on 2025-11-04 22:45:58 EET

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 889 (class 1247 OID 26838)
-- Name: bookingstatus; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.bookingstatus AS ENUM (
    'PENDING',
    'PENDING_VENDOR_APPROVAL',
    'CONFIRMED',
    'REJECTED',
    'CANCELLED',
    'COMPLETED'
);


--
-- TOC entry 886 (class 1247 OID 26831)
-- Name: userrole; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.userrole AS ENUM (
    'CUSTOMER',
    'VENDOR',
    'ADMIN'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 222 (class 1259 OID 26940)
-- Name: activities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activities (
    id integer NOT NULL,
    vendor_id integer NOT NULL,
    title character varying(500) NOT NULL,
    slug character varying(500) NOT NULL,
    description text,
    short_description text,
    price_adult numeric(10,2) NOT NULL,
    price_child numeric(10,2),
    price_currency character varying(3),
    duration_minutes integer,
    max_group_size integer,
    instant_confirmation boolean,
    free_cancellation_hours integer,
    languages character varying[],
    is_bestseller boolean,
    is_skip_the_line boolean,
    is_active boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    has_multiple_tiers boolean,
    discount_percentage integer,
    original_price_adult numeric(10,2),
    original_price_child numeric(10,2),
    is_likely_to_sell_out boolean,
    has_mobile_ticket boolean,
    has_best_price_guarantee boolean,
    is_verified_activity boolean,
    response_time_hours integer,
    is_wheelchair_accessible boolean,
    is_stroller_accessible boolean,
    allows_service_animals boolean,
    has_infant_seats boolean,
    video_url character varying(500),
    dress_code text,
    weather_dependent boolean,
    not_suitable_for text,
    what_to_bring text,
    has_covid_measures boolean,
    covid_measures text,
    is_giftable boolean,
    allows_reserve_now_pay_later boolean,
    reserve_payment_deadline_hours integer,
    average_rating numeric(2,1),
    total_reviews integer,
    total_bookings integer
);


--
-- TOC entry 221 (class 1259 OID 26939)
-- Name: activities_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.activities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4233 (class 0 OID 0)
-- Dependencies: 221
-- Name: activities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.activities_id_seq OWNED BY public.activities.id;


--
-- TOC entry 242 (class 1259 OID 27107)
-- Name: activity_add_ons; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_add_ons (
    id integer NOT NULL,
    activity_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    price numeric(10,2) NOT NULL,
    is_optional boolean,
    order_index integer
);


--
-- TOC entry 241 (class 1259 OID 27106)
-- Name: activity_add_ons_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.activity_add_ons_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4234 (class 0 OID 0)
-- Dependencies: 241
-- Name: activity_add_ons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.activity_add_ons_id_seq OWNED BY public.activity_add_ons.id;


--
-- TOC entry 267 (class 1259 OID 27361)
-- Name: activity_addon_translations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_addon_translations (
    id integer NOT NULL,
    addon_id integer NOT NULL,
    language character varying(2) NOT NULL,
    name character varying(255),
    description text
);


--
-- TOC entry 266 (class 1259 OID 27360)
-- Name: activity_addon_translations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.activity_addon_translations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4235 (class 0 OID 0)
-- Dependencies: 266
-- Name: activity_addon_translations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.activity_addon_translations_id_seq OWNED BY public.activity_addon_translations.id;


--
-- TOC entry 225 (class 1259 OID 26971)
-- Name: activity_categories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_categories (
    activity_id integer NOT NULL,
    category_id integer NOT NULL
);


--
-- TOC entry 226 (class 1259 OID 26986)
-- Name: activity_destinations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_destinations (
    activity_id integer NOT NULL,
    destination_id integer NOT NULL
);


--
-- TOC entry 261 (class 1259 OID 27310)
-- Name: activity_faq_translations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_faq_translations (
    id integer NOT NULL,
    faq_id integer NOT NULL,
    language character varying(2) NOT NULL,
    question text,
    answer text
);


--
-- TOC entry 260 (class 1259 OID 27309)
-- Name: activity_faq_translations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.activity_faq_translations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4236 (class 0 OID 0)
-- Dependencies: 260
-- Name: activity_faq_translations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.activity_faq_translations_id_seq OWNED BY public.activity_faq_translations.id;


--
-- TOC entry 232 (class 1259 OID 27032)
-- Name: activity_faqs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_faqs (
    id integer NOT NULL,
    activity_id integer NOT NULL,
    question text NOT NULL,
    answer text NOT NULL,
    order_index integer
);


--
-- TOC entry 231 (class 1259 OID 27031)
-- Name: activity_faqs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.activity_faqs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4237 (class 0 OID 0)
-- Dependencies: 231
-- Name: activity_faqs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.activity_faqs_id_seq OWNED BY public.activity_faqs.id;


--
-- TOC entry 257 (class 1259 OID 27276)
-- Name: activity_highlight_translations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_highlight_translations (
    id integer NOT NULL,
    highlight_id integer NOT NULL,
    language character varying(2) NOT NULL,
    text character varying(500)
);


--
-- TOC entry 256 (class 1259 OID 27275)
-- Name: activity_highlight_translations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.activity_highlight_translations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4238 (class 0 OID 0)
-- Dependencies: 256
-- Name: activity_highlight_translations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.activity_highlight_translations_id_seq OWNED BY public.activity_highlight_translations.id;


--
-- TOC entry 228 (class 1259 OID 27002)
-- Name: activity_highlights; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_highlights (
    id integer NOT NULL,
    activity_id integer NOT NULL,
    text character varying(500) NOT NULL,
    order_index integer
);


--
-- TOC entry 227 (class 1259 OID 27001)
-- Name: activity_highlights_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.activity_highlights_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4239 (class 0 OID 0)
-- Dependencies: 227
-- Name: activity_highlights_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.activity_highlights_id_seq OWNED BY public.activity_highlights.id;


--
-- TOC entry 224 (class 1259 OID 26957)
-- Name: activity_images; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_images (
    id integer NOT NULL,
    activity_id integer NOT NULL,
    url character varying(500) NOT NULL,
    alt_text character varying(255),
    caption text,
    is_primary boolean,
    is_hero boolean,
    order_index integer
);


--
-- TOC entry 223 (class 1259 OID 26956)
-- Name: activity_images_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.activity_images_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4240 (class 0 OID 0)
-- Dependencies: 223
-- Name: activity_images_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.activity_images_id_seq OWNED BY public.activity_images.id;


--
-- TOC entry 259 (class 1259 OID 27293)
-- Name: activity_include_translations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_include_translations (
    id integer NOT NULL,
    include_id integer NOT NULL,
    language character varying(2) NOT NULL,
    item character varying(500)
);


--
-- TOC entry 258 (class 1259 OID 27292)
-- Name: activity_include_translations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.activity_include_translations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4241 (class 0 OID 0)
-- Dependencies: 258
-- Name: activity_include_translations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.activity_include_translations_id_seq OWNED BY public.activity_include_translations.id;


--
-- TOC entry 230 (class 1259 OID 27017)
-- Name: activity_includes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_includes (
    id integer NOT NULL,
    activity_id integer NOT NULL,
    item character varying(500) NOT NULL,
    is_included boolean,
    order_index integer
);


--
-- TOC entry 229 (class 1259 OID 27016)
-- Name: activity_includes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.activity_includes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4242 (class 0 OID 0)
-- Dependencies: 229
-- Name: activity_includes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.activity_includes_id_seq OWNED BY public.activity_includes.id;


--
-- TOC entry 265 (class 1259 OID 27344)
-- Name: activity_pricing_tier_translations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_pricing_tier_translations (
    id integer NOT NULL,
    pricing_tier_id integer NOT NULL,
    language character varying(2) NOT NULL,
    tier_name character varying(100),
    tier_description text
);


--
-- TOC entry 264 (class 1259 OID 27343)
-- Name: activity_pricing_tier_translations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.activity_pricing_tier_translations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4243 (class 0 OID 0)
-- Dependencies: 264
-- Name: activity_pricing_tier_translations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.activity_pricing_tier_translations_id_seq OWNED BY public.activity_pricing_tier_translations.id;


--
-- TOC entry 240 (class 1259 OID 27092)
-- Name: activity_pricing_tiers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_pricing_tiers (
    id integer NOT NULL,
    activity_id integer NOT NULL,
    tier_name character varying(100) NOT NULL,
    tier_description text,
    price_adult numeric(10,2) NOT NULL,
    price_child numeric(10,2),
    order_index integer,
    is_active boolean
);


--
-- TOC entry 239 (class 1259 OID 27091)
-- Name: activity_pricing_tiers_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.activity_pricing_tiers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4244 (class 0 OID 0)
-- Dependencies: 239
-- Name: activity_pricing_tiers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.activity_pricing_tiers_id_seq OWNED BY public.activity_pricing_tiers.id;


--
-- TOC entry 238 (class 1259 OID 27079)
-- Name: activity_time_slots; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_time_slots (
    id integer NOT NULL,
    activity_id integer NOT NULL,
    slot_time character varying(5) NOT NULL,
    slot_label character varying(50),
    max_capacity integer,
    is_available boolean,
    price_adjustment numeric(10,2)
);


--
-- TOC entry 237 (class 1259 OID 27078)
-- Name: activity_time_slots_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.activity_time_slots_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4245 (class 0 OID 0)
-- Dependencies: 237
-- Name: activity_time_slots_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.activity_time_slots_id_seq OWNED BY public.activity_time_slots.id;


--
-- TOC entry 263 (class 1259 OID 27327)
-- Name: activity_timeline_translations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_timeline_translations (
    id integer NOT NULL,
    timeline_id integer NOT NULL,
    language character varying(2) NOT NULL,
    title character varying(255),
    description text
);


--
-- TOC entry 262 (class 1259 OID 27326)
-- Name: activity_timeline_translations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.activity_timeline_translations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4246 (class 0 OID 0)
-- Dependencies: 262
-- Name: activity_timeline_translations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.activity_timeline_translations_id_seq OWNED BY public.activity_timeline_translations.id;


--
-- TOC entry 236 (class 1259 OID 27064)
-- Name: activity_timelines; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_timelines (
    id integer NOT NULL,
    activity_id integer NOT NULL,
    step_number integer NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    duration_minutes integer,
    image_url character varying(500),
    order_index integer
);


--
-- TOC entry 235 (class 1259 OID 27063)
-- Name: activity_timelines_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.activity_timelines_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4247 (class 0 OID 0)
-- Dependencies: 235
-- Name: activity_timelines_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.activity_timelines_id_seq OWNED BY public.activity_timelines.id;


--
-- TOC entry 249 (class 1259 OID 27183)
-- Name: activity_translations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_translations (
    id integer NOT NULL,
    activity_id integer NOT NULL,
    language character varying(2) NOT NULL,
    title character varying(500),
    short_description text,
    description text,
    dress_code text,
    what_to_bring text,
    not_suitable_for text,
    covid_measures text,
    cancellation_policy text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


--
-- TOC entry 248 (class 1259 OID 27182)
-- Name: activity_translations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.activity_translations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4248 (class 0 OID 0)
-- Dependencies: 248
-- Name: activity_translations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.activity_translations_id_seq OWNED BY public.activity_translations.id;


--
-- TOC entry 246 (class 1259 OID 27152)
-- Name: availability; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.availability (
    id integer NOT NULL,
    activity_id integer NOT NULL,
    date date NOT NULL,
    start_time time without time zone,
    end_time time without time zone,
    spots_available integer,
    spots_total integer,
    price_adult numeric(10,2),
    price_child numeric(10,2),
    is_available boolean
);


--
-- TOC entry 245 (class 1259 OID 27151)
-- Name: availability_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.availability_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4249 (class 0 OID 0)
-- Dependencies: 245
-- Name: availability_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.availability_id_seq OWNED BY public.availability.id;


--
-- TOC entry 244 (class 1259 OID 27122)
-- Name: bookings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bookings (
    id integer NOT NULL,
    booking_ref character varying(20) NOT NULL,
    user_id integer,
    activity_id integer NOT NULL,
    vendor_id integer NOT NULL,
    booking_date date NOT NULL,
    booking_time time without time zone,
    adults integer,
    children integer,
    total_participants integer NOT NULL,
    price_per_adult numeric(10,2),
    price_per_child numeric(10,2),
    total_price numeric(10,2) NOT NULL,
    currency character varying(3),
    status public.bookingstatus NOT NULL,
    customer_name character varying(255),
    customer_email character varying(255),
    customer_phone character varying(50),
    special_requirements text,
    rejection_reason text,
    created_at timestamp with time zone DEFAULT now(),
    confirmed_at timestamp with time zone,
    vendor_approved_at timestamp with time zone,
    vendor_rejected_at timestamp with time zone,
    cancelled_at timestamp with time zone,
    completed_at timestamp with time zone
);


--
-- TOC entry 243 (class 1259 OID 27121)
-- Name: bookings_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bookings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4250 (class 0 OID 0)
-- Dependencies: 243
-- Name: bookings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bookings_id_seq OWNED BY public.bookings.id;


--
-- TOC entry 253 (class 1259 OID 27216)
-- Name: cart_items; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cart_items (
    id integer NOT NULL,
    session_id character varying(255) NOT NULL,
    activity_id integer NOT NULL,
    booking_date date NOT NULL,
    booking_time time without time zone,
    adults integer,
    children integer,
    price numeric(10,2),
    time_slot_id integer,
    pricing_tier_id integer,
    add_on_ids text,
    add_on_quantities text,
    created_at timestamp with time zone DEFAULT now()
);


--
-- TOC entry 252 (class 1259 OID 27215)
-- Name: cart_items_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cart_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4251 (class 0 OID 0)
-- Dependencies: 252
-- Name: cart_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cart_items_id_seq OWNED BY public.cart_items.id;


--
-- TOC entry 212 (class 1259 OID 26864)
-- Name: categories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL,
    icon character varying(50),
    parent_id integer,
    order_index integer
);


--
-- TOC entry 211 (class 1259 OID 26863)
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4252 (class 0 OID 0)
-- Dependencies: 211
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- TOC entry 218 (class 1259 OID 26908)
-- Name: category_translations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.category_translations (
    id integer NOT NULL,
    category_id integer NOT NULL,
    language character varying(2) NOT NULL,
    name character varying(100) NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


--
-- TOC entry 217 (class 1259 OID 26907)
-- Name: category_translations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.category_translations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4253 (class 0 OID 0)
-- Dependencies: 217
-- Name: category_translations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.category_translations_id_seq OWNED BY public.category_translations.id;


--
-- TOC entry 220 (class 1259 OID 26924)
-- Name: destination_translations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.destination_translations (
    id integer NOT NULL,
    destination_id integer NOT NULL,
    language character varying(2) NOT NULL,
    name character varying(255) NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


--
-- TOC entry 219 (class 1259 OID 26923)
-- Name: destination_translations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.destination_translations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4254 (class 0 OID 0)
-- Dependencies: 219
-- Name: destination_translations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.destination_translations_id_seq OWNED BY public.destination_translations.id;


--
-- TOC entry 214 (class 1259 OID 26878)
-- Name: destinations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.destinations (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    country character varying(100),
    country_code character varying(2),
    image_url character varying(500),
    latitude double precision,
    longitude double precision,
    is_featured boolean,
    created_at timestamp with time zone DEFAULT now()
);


--
-- TOC entry 213 (class 1259 OID 26877)
-- Name: destinations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.destinations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4255 (class 0 OID 0)
-- Dependencies: 213
-- Name: destinations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.destinations_id_seq OWNED BY public.destinations.id;


--
-- TOC entry 251 (class 1259 OID 27201)
-- Name: meeting_point_photos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.meeting_point_photos (
    id integer NOT NULL,
    meeting_point_id integer NOT NULL,
    url character varying(500) NOT NULL,
    caption character varying(255),
    order_index integer
);


--
-- TOC entry 250 (class 1259 OID 27200)
-- Name: meeting_point_photos_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.meeting_point_photos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4256 (class 0 OID 0)
-- Dependencies: 250
-- Name: meeting_point_photos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.meeting_point_photos_id_seq OWNED BY public.meeting_point_photos.id;


--
-- TOC entry 269 (class 1259 OID 27378)
-- Name: meeting_point_translations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.meeting_point_translations (
    id integer NOT NULL,
    meeting_point_id integer NOT NULL,
    language character varying(2) NOT NULL,
    address text,
    instructions text,
    parking_info text,
    public_transport_info text,
    nearby_landmarks text
);


--
-- TOC entry 268 (class 1259 OID 27377)
-- Name: meeting_point_translations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.meeting_point_translations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4257 (class 0 OID 0)
-- Dependencies: 268
-- Name: meeting_point_translations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.meeting_point_translations_id_seq OWNED BY public.meeting_point_translations.id;


--
-- TOC entry 234 (class 1259 OID 27047)
-- Name: meeting_points; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.meeting_points (
    id integer NOT NULL,
    activity_id integer NOT NULL,
    address text NOT NULL,
    instructions text,
    latitude double precision,
    longitude double precision,
    parking_info text,
    public_transport_info text,
    nearby_landmarks text
);


--
-- TOC entry 233 (class 1259 OID 27046)
-- Name: meeting_points_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.meeting_points_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4258 (class 0 OID 0)
-- Dependencies: 233
-- Name: meeting_points_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.meeting_points_id_seq OWNED BY public.meeting_points.id;


--
-- TOC entry 273 (class 1259 OID 27410)
-- Name: review_categories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.review_categories (
    id integer NOT NULL,
    review_id integer NOT NULL,
    category_name character varying(100) NOT NULL,
    rating integer NOT NULL,
    CONSTRAINT ck_review_categories_check_category_rating_range CHECK (((rating >= 1) AND (rating <= 5)))
);


--
-- TOC entry 272 (class 1259 OID 27409)
-- Name: review_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.review_categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4259 (class 0 OID 0)
-- Dependencies: 272
-- Name: review_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.review_categories_id_seq OWNED BY public.review_categories.id;


--
-- TOC entry 271 (class 1259 OID 27395)
-- Name: review_images; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.review_images (
    id integer NOT NULL,
    review_id integer NOT NULL,
    url character varying(500) NOT NULL,
    caption character varying(255)
);


--
-- TOC entry 270 (class 1259 OID 27394)
-- Name: review_images_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.review_images_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4260 (class 0 OID 0)
-- Dependencies: 270
-- Name: review_images_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.review_images_id_seq OWNED BY public.review_images.id;


--
-- TOC entry 255 (class 1259 OID 27244)
-- Name: reviews; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.reviews (
    id integer NOT NULL,
    booking_id integer,
    user_id integer NOT NULL,
    activity_id integer NOT NULL,
    vendor_id integer NOT NULL,
    rating integer NOT NULL,
    title character varying(255),
    comment text,
    is_verified_booking boolean,
    helpful_count integer,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    CONSTRAINT ck_reviews_check_rating_range CHECK (((rating >= 1) AND (rating <= 5)))
);


--
-- TOC entry 254 (class 1259 OID 27243)
-- Name: reviews_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.reviews_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4261 (class 0 OID 0)
-- Dependencies: 254
-- Name: reviews_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.reviews_id_seq OWNED BY public.reviews.id;


--
-- TOC entry 210 (class 1259 OID 26852)
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    full_name character varying(255) NOT NULL,
    phone character varying(50),
    role public.userrole NOT NULL,
    email_verified boolean,
    is_active boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


--
-- TOC entry 209 (class 1259 OID 26851)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4262 (class 0 OID 0)
-- Dependencies: 209
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 216 (class 1259 OID 26890)
-- Name: vendors; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vendors (
    id integer NOT NULL,
    user_id integer NOT NULL,
    company_name character varying(255) NOT NULL,
    description character varying,
    logo_url character varying(500),
    commission_rate numeric(5,2),
    is_verified boolean,
    verified_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now()
);


--
-- TOC entry 215 (class 1259 OID 26889)
-- Name: vendors_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.vendors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4263 (class 0 OID 0)
-- Dependencies: 215
-- Name: vendors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.vendors_id_seq OWNED BY public.vendors.id;


--
-- TOC entry 247 (class 1259 OID 27166)
-- Name: wishlist; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.wishlist (
    user_id integer NOT NULL,
    activity_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


--
-- TOC entry 3814 (class 2604 OID 26943)
-- Name: activities id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activities ALTER COLUMN id SET DEFAULT nextval('public.activities_id_seq'::regclass);


--
-- TOC entry 3824 (class 2604 OID 27110)
-- Name: activity_add_ons id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_add_ons ALTER COLUMN id SET DEFAULT nextval('public.activity_add_ons_id_seq'::regclass);


--
-- TOC entry 3842 (class 2604 OID 27364)
-- Name: activity_addon_translations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_addon_translations ALTER COLUMN id SET DEFAULT nextval('public.activity_addon_translations_id_seq'::regclass);


--
-- TOC entry 3839 (class 2604 OID 27313)
-- Name: activity_faq_translations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_faq_translations ALTER COLUMN id SET DEFAULT nextval('public.activity_faq_translations_id_seq'::regclass);


--
-- TOC entry 3819 (class 2604 OID 27035)
-- Name: activity_faqs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_faqs ALTER COLUMN id SET DEFAULT nextval('public.activity_faqs_id_seq'::regclass);


--
-- TOC entry 3837 (class 2604 OID 27279)
-- Name: activity_highlight_translations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_highlight_translations ALTER COLUMN id SET DEFAULT nextval('public.activity_highlight_translations_id_seq'::regclass);


--
-- TOC entry 3817 (class 2604 OID 27005)
-- Name: activity_highlights id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_highlights ALTER COLUMN id SET DEFAULT nextval('public.activity_highlights_id_seq'::regclass);


--
-- TOC entry 3816 (class 2604 OID 26960)
-- Name: activity_images id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_images ALTER COLUMN id SET DEFAULT nextval('public.activity_images_id_seq'::regclass);


--
-- TOC entry 3838 (class 2604 OID 27296)
-- Name: activity_include_translations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_include_translations ALTER COLUMN id SET DEFAULT nextval('public.activity_include_translations_id_seq'::regclass);


--
-- TOC entry 3818 (class 2604 OID 27020)
-- Name: activity_includes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_includes ALTER COLUMN id SET DEFAULT nextval('public.activity_includes_id_seq'::regclass);


--
-- TOC entry 3841 (class 2604 OID 27347)
-- Name: activity_pricing_tier_translations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_pricing_tier_translations ALTER COLUMN id SET DEFAULT nextval('public.activity_pricing_tier_translations_id_seq'::regclass);


--
-- TOC entry 3823 (class 2604 OID 27095)
-- Name: activity_pricing_tiers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_pricing_tiers ALTER COLUMN id SET DEFAULT nextval('public.activity_pricing_tiers_id_seq'::regclass);


--
-- TOC entry 3822 (class 2604 OID 27082)
-- Name: activity_time_slots id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_time_slots ALTER COLUMN id SET DEFAULT nextval('public.activity_time_slots_id_seq'::regclass);


--
-- TOC entry 3840 (class 2604 OID 27330)
-- Name: activity_timeline_translations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_timeline_translations ALTER COLUMN id SET DEFAULT nextval('public.activity_timeline_translations_id_seq'::regclass);


--
-- TOC entry 3821 (class 2604 OID 27067)
-- Name: activity_timelines id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_timelines ALTER COLUMN id SET DEFAULT nextval('public.activity_timelines_id_seq'::regclass);


--
-- TOC entry 3829 (class 2604 OID 27186)
-- Name: activity_translations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_translations ALTER COLUMN id SET DEFAULT nextval('public.activity_translations_id_seq'::regclass);


--
-- TOC entry 3827 (class 2604 OID 27155)
-- Name: availability id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.availability ALTER COLUMN id SET DEFAULT nextval('public.availability_id_seq'::regclass);


--
-- TOC entry 3825 (class 2604 OID 27125)
-- Name: bookings id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bookings ALTER COLUMN id SET DEFAULT nextval('public.bookings_id_seq'::regclass);


--
-- TOC entry 3832 (class 2604 OID 27219)
-- Name: cart_items id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart_items ALTER COLUMN id SET DEFAULT nextval('public.cart_items_id_seq'::regclass);


--
-- TOC entry 3805 (class 2604 OID 26867)
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- TOC entry 3810 (class 2604 OID 26911)
-- Name: category_translations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.category_translations ALTER COLUMN id SET DEFAULT nextval('public.category_translations_id_seq'::regclass);


--
-- TOC entry 3812 (class 2604 OID 26927)
-- Name: destination_translations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.destination_translations ALTER COLUMN id SET DEFAULT nextval('public.destination_translations_id_seq'::regclass);


--
-- TOC entry 3806 (class 2604 OID 26881)
-- Name: destinations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.destinations ALTER COLUMN id SET DEFAULT nextval('public.destinations_id_seq'::regclass);


--
-- TOC entry 3831 (class 2604 OID 27204)
-- Name: meeting_point_photos id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meeting_point_photos ALTER COLUMN id SET DEFAULT nextval('public.meeting_point_photos_id_seq'::regclass);


--
-- TOC entry 3843 (class 2604 OID 27381)
-- Name: meeting_point_translations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meeting_point_translations ALTER COLUMN id SET DEFAULT nextval('public.meeting_point_translations_id_seq'::regclass);


--
-- TOC entry 3820 (class 2604 OID 27050)
-- Name: meeting_points id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meeting_points ALTER COLUMN id SET DEFAULT nextval('public.meeting_points_id_seq'::regclass);


--
-- TOC entry 3845 (class 2604 OID 27413)
-- Name: review_categories id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.review_categories ALTER COLUMN id SET DEFAULT nextval('public.review_categories_id_seq'::regclass);


--
-- TOC entry 3844 (class 2604 OID 27398)
-- Name: review_images id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.review_images ALTER COLUMN id SET DEFAULT nextval('public.review_images_id_seq'::regclass);


--
-- TOC entry 3834 (class 2604 OID 27247)
-- Name: reviews id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviews ALTER COLUMN id SET DEFAULT nextval('public.reviews_id_seq'::regclass);


--
-- TOC entry 3803 (class 2604 OID 26855)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 3808 (class 2604 OID 26893)
-- Name: vendors id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vendors ALTER COLUMN id SET DEFAULT nextval('public.vendors_id_seq'::regclass);


--
-- TOC entry 4176 (class 0 OID 26940)
-- Dependencies: 222
-- Data for Name: activities; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activities (id, vendor_id, title, slug, description, short_description, price_adult, price_child, price_currency, duration_minutes, max_group_size, instant_confirmation, free_cancellation_hours, languages, is_bestseller, is_skip_the_line, is_active, created_at, updated_at, has_multiple_tiers, discount_percentage, original_price_adult, original_price_child, is_likely_to_sell_out, has_mobile_ticket, has_best_price_guarantee, is_verified_activity, response_time_hours, is_wheelchair_accessible, is_stroller_accessible, allows_service_animals, has_infant_seats, video_url, dress_code, weather_dependent, not_suitable_for, what_to_bring, has_covid_measures, covid_measures, is_giftable, allows_reserve_now_pay_later, reserve_payment_deadline_hours, average_rating, total_reviews, total_bookings) FROM stdin;
1	1	Great Wall of China Private Day Tour with Lunch	great-wall-private-tour-beijing	Experience one of the world's most iconic landmarks on this private Great Wall tour. Visit the well-preserved Mutianyu section, known for its stunning mountain scenery and fewer crowds. Your expert local guide will share fascinating stories about this UNESCO World Heritage site while you walk along the ancient walls. Includes round-trip transportation, cable car tickets, and authentic Chinese lunch.	Explore the magnificent Great Wall at Mutianyu section with private guide and traditional Chinese lunch	89.00	62.30	EUR	480	10	t	24	{english,chinese}	f	t	t	2025-11-03 16:32:47.916739+02	2025-11-03 20:35:18.977691+02	f	\N	\N	\N	f	t	t	t	24	t	f	t	f	\N	\N	f	\N	Comfortable walking shoes, weather-appropriate clothing, camera, water bottle	t	Face masks required in enclosed spaces, hand sanitizer provided, reduced group sizes	t	t	24	4.4	10	24
2	3	Shanghai Food Tour: Local Street Food and Hidden Gems	shanghai-food-tour-street-food	Embark on a culinary adventure through Shanghai's vibrant food scene. This guided tour takes you beyond tourist restaurants to discover authentic local flavors. Visit bustling wet markets, historic food streets, and hidden gems known only to locals. Taste traditional dishes like xiaolongbao (soup dumplings), shengjianbao (pan-fried pork buns), and other Shanghainese specialties while learning about the city's rich culinary heritage.	Discover authentic Shanghai flavors on this guided food tour through local markets and street food stalls	65.00	45.50	EUR	240	18	t	24	{english,chinese}	t	t	t	2025-11-03 16:32:47.916739+02	2025-11-03 20:35:18.977691+02	f	\N	\N	\N	f	t	t	t	24	f	t	t	f	\N	\N	f	\N	Comfortable walking shoes, weather-appropriate clothing, camera, water bottle	t	Face masks required in enclosed spaces, hand sanitizer provided, reduced group sizes	t	t	24	4.4	10	16
3	2	Stockholm University Campus & Swedish Education System Study Tour	stockholm-university-study-tour	Immerse yourself in the renowned Swedish education system on this comprehensive study tour. Visit Stockholm University campus, meet with international students and professors, and learn about Sweden's innovative approach to higher education. This educational experience is perfect for students, educators, and anyone interested in Nordic educational excellence. Includes campus tours, interactive sessions, and insights into Swedish academic culture.	Explore Swedish higher education system with university visits, student interactions, and education insights	120.00	84.00	EUR	360	13	t	24	{english,chinese}	t	f	t	2025-11-03 16:32:47.916739+02	2025-11-03 20:35:18.977691+02	f	\N	\N	\N	f	t	t	t	24	f	f	t	f	\N	\N	f	\N	Comfortable walking shoes, weather-appropriate clothing, camera, water bottle	t	Face masks required in enclosed spaces, hand sanitizer provided, reduced group sizes	t	t	24	4.4	10	20
4	4	Copenhagen Design Academy & Danish Design Philosophy Workshop	copenhagen-design-academy-workshop	Discover the secrets behind Denmark's world-renowned design philosophy in this immersive educational experience. Visit the Danish Design Academy, participate in hands-on workshops, and meet with professional designers. Learn about hygge, functionality, and minimalism that define Danish design. This study tour combines theoretical knowledge with practical experience, perfect for design students, professionals, and enthusiasts.	Learn Danish design principles through academy visits, hands-on workshops, and designer meetings	95.00	66.50	EUR	300	12	t	24	{english,chinese}	t	f	t	2025-11-03 16:32:47.916739+02	2025-11-03 20:35:18.977691+02	f	\N	\N	\N	f	t	t	t	24	f	f	t	f	\N	\N	f	\N	Comfortable walking shoes, weather-appropriate clothing, camera, water bottle	t	Face masks required in enclosed spaces, hand sanitizer provided, reduced group sizes	t	t	24	4.4	10	22
5	6	Northern Lights Chase & Arctic Culture Experience	oslo-northern-lights-arctic-culture	Embark on an unforgettable Northern Lights adventure combined with authentic Arctic cultural experiences. Journey from Oslo to prime aurora viewing locations while learning about Sami indigenous culture, Arctic wildlife, and traditional Nordic survival skills. This tour includes traditional reindeer stew dinner, warm arctic clothing, and professional aurora photography guidance.	Hunt for Northern Lights while learning about Sami culture and Arctic traditions	145.00	101.50	EUR	480	17	t	24	{english,chinese}	f	f	t	2025-11-03 16:32:47.916739+02	2025-11-03 20:35:18.977691+02	f	\N	\N	\N	f	t	t	t	24	f	t	t	f	\N	\N	f	\N	Comfortable walking shoes, weather-appropriate clothing, camera, water bottle	t	Face masks required in enclosed spaces, hand sanitizer provided, reduced group sizes	t	t	24	4.4	10	29
6	5	Xi'an Terracotta Army Discovery Tour with Ancient History	xian-terracotta-warriors-history-tour	Step into ancient China on this comprehensive Terracotta Army tour. Discover the incredible archaeological site where thousands of life-sized warrior statues guard Emperor Qin's tomb. Your expert guide, with archaeological background, will reveal the latest discoveries and historical significance. Visit all three excavation pits, the Bronze Chariot Exhibition, and learn about the Qin Dynasty's remarkable achievements.	Explore the legendary Terracotta Army with expert archaeological insights and ancient Chinese history	75.00	52.50	EUR	360	19	t	24	{english,chinese}	f	t	t	2025-11-03 16:32:47.916739+02	2025-11-03 20:35:18.977691+02	f	\N	\N	\N	f	t	t	t	24	t	f	t	f	\N	\N	f	\N	Comfortable walking shoes, weather-appropriate clothing, camera, water bottle	t	Face masks required in enclosed spaces, hand sanitizer provided, reduced group sizes	t	t	24	4.4	10	14
8	8	Sichuan Culinary Institute Cooking Masterclass	sichuan-culinary-masterclass-chengdu	Immerse yourself in the fiery world of Sichuan cuisine with this comprehensive cooking masterclass at Chengdu's renowned culinary institute. Learn to prepare traditional dishes like Mapo Tofu, Kung Pao Chicken, and Dan Dan Noodles from certified Sichuan chefs. Understand the art of balancing the famous 'mala' (numbing and spicy) flavors, source ingredients at local markets, and take home authentic recipes and techniques.	Learn authentic Sichuan cuisine from professional chefs in Chengdu's premier culinary institute	120.00	84.00	EUR	360	15	t	24	{english,chinese,spanish}	t	t	t	2025-09-05 17:27:28.741081+03	2025-11-03 20:35:18.977691+02	t	\N	144.00	100.80	t	t	t	t	2	t	f	t	t	\N	Casual comfortable clothing recommended	t	\N	Camera, comfortable walking shoes, sun protection	t	Regular sanitization, masks available, temperature checks	t	t	48	4.6	12	0
9	8	Zhangjiajie Avatar Mountain Photography Adventure	zhangjiajie-avatar-mountain-photography	Explore the mystical landscape that inspired James Cameron's Avatar in this photography-focused adventure through Zhangjiajie National Forest Park. Navigate through towering sandstone pillars, misty valleys, and ancient forests with a professional landscape photographer as your guide. Learn advanced photography techniques while capturing stunning shots of the world's most unique geological formations.	Capture the otherworldly beauty of Zhangjiajie's pillars that inspired Avatar's Pandora	180.00	126.00	EUR	600	9	t	24	{english,chinese,spanish}	f	f	t	2025-07-12 17:27:29.429844+03	2025-11-03 20:35:18.977691+02	t	\N	216.00	151.20	f	t	t	t	2	f	t	t	f	\N	Casual comfortable clothing recommended	t	\N	Camera, comfortable walking shoes, sun protection	t	Regular sanitization, masks available, temperature checks	t	t	48	4.6	12	0
10	8	Beijing Traditional Arts & Temple Culture Experience	beijing-traditional-arts-temple-culture	Discover the spiritual and artistic heart of Beijing through this immersive cultural journey. Visit historic temples including the Temple of Heaven, participate in traditional Chinese art workshops like calligraphy and paper cutting, and meet master craftsmen who preserve ancient techniques. Experience tea ceremony, learn about feng shui principles, and understand the philosophy behind Chinese traditional arts.	Explore ancient Beijing through traditional arts, temple visits, and master craftsman workshops	85.00	59.50	EUR	420	14	t	24	{english,chinese,spanish}	f	t	t	2025-08-12 17:27:29.446285+03	2025-11-03 20:35:18.977691+02	t	\N	102.00	71.40	f	t	t	t	2	f	f	t	t	\N	Casual comfortable clothing recommended	t	\N	Camera, comfortable walking shoes, sun protection	t	Regular sanitization, masks available, temperature checks	t	t	48	4.6	12	0
11	8	Guangzhou Modern Art & Innovation District Tour	guangzhou-modern-art-innovation-district	Discover modern China through Guangzhou's thriving contemporary art scene and cutting-edge urban development. Visit world-class galleries, meet local artists in their studios, explore innovative architectural projects, and understand how traditional Chinese culture adapts to modern urban life. This tour showcases China's creative renaissance and urban innovation.	Explore Guangzhou's contemporary art scene and innovative urban development	75.00	52.50	EUR	300	10	t	24	{english,chinese,spanish}	f	f	t	2025-06-05 17:27:29.456666+03	2025-11-03 20:35:18.977691+02	t	19	90.00	63.00	f	t	t	t	2	t	t	t	t	\N	Casual comfortable clothing recommended	t	\N	Camera, comfortable walking shoes, sun protection	t	Regular sanitization, masks available, temperature checks	t	t	48	4.6	12	0
12	8	Shanghai Street Food & Night Market Adventure	shanghai-street-food-night-market-adventure	Experience Shanghai after dark through its bustling night markets and street food scene. Follow local food guides through hidden alleys and popular markets, sampling everything from xiaolongbao to grilled squid. Learn about Shanghai's culinary history, meet local vendors, and discover foods you won't find in restaurants. This authentic food adventure reveals the real taste of Shanghai.	Navigate Shanghai's vibrant night markets and discover authentic street food treasures	65.00	45.50	EUR	240	9	t	24	{english,chinese,spanish}	t	t	t	2025-05-15 17:27:29.467129+03	2025-11-03 20:35:18.977691+02	t	\N	78.00	54.60	f	t	t	t	2	t	t	t	t	\N	Casual comfortable clothing recommended	t	\N	Camera, comfortable walking shoes, sun protection	t	Regular sanitization, masks available, temperature checks	t	t	48	4.6	12	0
13	8	Guilin Li River Bamboo Rafting & Countryside	guilin-li-river-bamboo-rafting-countryside	Float through one of China's most iconic landscapes on a traditional bamboo raft along the Li River. Witness the dramatic karst peaks that have inspired Chinese artists for centuries, visit traditional fishing villages, and experience rural Chinese life. Learn about local customs, try your hand at cormorant fishing, and enjoy a countryside lunch with a local family.	Peaceful bamboo raft journey through Guilin's legendary karst landscapes and rural villages	95.00	66.50	EUR	480	9	t	24	{english,chinese,spanish}	t	t	t	2025-06-20 17:27:29.478148+03	2025-11-03 20:35:18.977691+02	t	\N	114.00	79.80	f	t	t	t	2	f	f	t	t	\N	Casual comfortable clothing recommended	t	\N	Camera, comfortable walking shoes, sun protection	t	Regular sanitization, masks available, temperature checks	t	t	48	4.6	12	0
14	8	Hangzhou West Lake Cultural Heritage Walk	hangzhou-west-lake-cultural-heritage-walk	Explore the poetic beauty of Hangzhou's West Lake, a UNESCO World Heritage site that has inspired poets and artists for over 1000 years. Walk along ancient causeways, visit historic temples and pagodas, and learn about the legends and literature associated with this legendary lake. Experience traditional Chinese garden design and understand why West Lake is considered paradise on earth.	Discover the UNESCO World Heritage beauty of West Lake and its cultural significance	70.00	49.00	EUR	300	9	t	24	{english,chinese,spanish}	f	t	t	2025-07-21 17:27:29.487266+03	2025-11-03 20:35:18.977691+02	t	\N	84.00	58.80	t	t	t	t	2	f	t	t	t	\N	Casual comfortable clothing recommended	t	\N	Camera, comfortable walking shoes, sun protection	t	Regular sanitization, masks available, temperature checks	t	t	48	4.6	12	0
15	8	Xi'an Silk Road History & Muslim Quarter Experience	xian-silk-road-history-muslim-quarter	Discover Xi'an's role as the starting point of the ancient Silk Road through its historic Muslim Quarter. Explore the Great Mosque, sample Halal Chinese cuisine, learn about the cultural exchange between East and West, and understand how different cultures have shaped this ancient capital. Visit traditional crafts workshops and experience the multicultural heritage of the Silk Road.	Journey through Xi'an's Silk Road heritage and vibrant Muslim cultural quarter	80.00	56.00	EUR	360	15	t	24	{english,chinese,spanish}	f	t	t	2025-09-18 17:27:29.494624+03	2025-11-03 20:35:18.977691+02	t	13	96.00	67.20	f	t	t	t	2	t	f	t	t	\N	Casual comfortable clothing recommended	t	\N	Camera, comfortable walking shoes, sun protection	t	Regular sanitization, masks available, temperature checks	t	t	48	4.6	12	0
16	8	University of Oslo Sustainability & Green Technology Study Program	university-oslo-sustainability-green-tech-study	Immerse yourself in Norway's pioneering approach to sustainability and green technology through this comprehensive study program at University of Oslo. Meet with professors and researchers working on climate solutions, visit cutting-edge laboratories, participate in workshops on renewable energy and environmental policy, and understand how Norway leads the world in sustainable development.	Learn from Norway's leading sustainability experts at University of Oslo's environmental programs	150.00	105.00	EUR	420	8	t	24	{english,chinese,spanish}	t	f	t	2025-08-24 17:27:29.502691+03	2025-11-03 20:35:18.977691+02	t	\N	180.00	126.00	t	t	t	t	2	t	f	t	t	\N	Casual comfortable clothing recommended	t	\N	Camera, comfortable walking shoes, sun protection	t	Regular sanitization, masks available, temperature checks	t	t	48	4.6	12	0
17	8	Finnish Innovation Hub & Startup Ecosystem Study Tour	finnish-innovation-startup-ecosystem-study	Discover what makes Finland one of the world's most innovative countries through visits to leading tech companies, startup incubators, and research institutions in Helsinki. Meet with successful entrepreneurs, participate in innovation workshops, learn about Finland's education system that fosters creativity, and understand the Nordic approach to work-life balance and innovation culture.	Explore Finland's world-renowned innovation ecosystem and startup culture in Helsinki	140.00	98.00	EUR	360	14	t	24	{english,chinese,spanish}	f	t	t	2025-09-26 17:27:29.511689+03	2025-11-03 20:35:18.977691+02	t	23	168.00	117.60	f	t	t	t	2	t	f	t	t	\N	Casual comfortable clothing recommended	t	\N	Camera, comfortable walking shoes, sun protection	t	Regular sanitization, masks available, temperature checks	t	t	48	4.6	12	0
18	8	Danish Language & Culture Immersion Experience	danish-language-culture-immersion-copenhagen	Experience total Danish language and cultural immersion through this comprehensive program in Copenhagen. Participate in intensive language classes with native speakers, live with local families, explore Danish cultural institutions, and practice your skills in real-world situations. Learn about hygge culture, Danish social values, and the Danish approach to happiness and community.	Intensive Danish language learning combined with deep cultural immersion in Copenhagen	110.00	77.00	EUR	480	9	t	24	{english,chinese,spanish}	f	t	t	2025-09-22 17:27:29.526328+03	2025-11-03 20:35:18.977691+02	t	\N	132.00	92.40	f	t	t	t	2	f	t	t	t	\N	Casual comfortable clothing recommended	t	\N	Camera, comfortable walking shoes, sun protection	t	Regular sanitization, masks available, temperature checks	t	t	48	4.6	12	0
19	8	Swedish Education System & Teaching Methods Study Tour	swedish-education-system-teaching-methods-study	Discover the secrets behind Sweden's world-class education system through visits to schools, universities, and educational research centers in Stockholm. Observe classes in action, meet with teachers and education experts, learn about Swedish pedagogical approaches, and understand how Sweden creates inclusive, innovative learning environments that consistently rank among the world's best.	Explore Sweden's progressive education system and innovative teaching methodologies	135.00	94.50	EUR	390	8	t	24	{english,chinese,spanish}	f	t	t	2025-08-17 17:27:29.534473+03	2025-11-03 20:35:18.977691+02	t	\N	162.00	113.40	t	t	t	t	2	t	f	t	f	\N	Casual comfortable clothing recommended	t	\N	Camera, comfortable walking shoes, sun protection	t	Regular sanitization, masks available, temperature checks	t	t	48	4.6	12	0
20	8	Norwegian Fjords & Arctic Wildlife Photography Expedition	norwegian-fjords-arctic-wildlife-photography	Embark on an unforgettable photography expedition through Norway's most spectacular fjords and Arctic regions. Learn from professional wildlife photographers while capturing images of seals, whales, Arctic birds, and the dramatic landscapes of the Norwegian coast. Experience the midnight sun or northern lights depending on season, and master techniques for extreme weather photography.	Capture the raw beauty of Norwegian fjords and Arctic wildlife on this photography expedition	220.00	154.00	EUR	600	13	t	24	{english,chinese,spanish}	f	f	t	2025-08-13 17:27:29.54279+03	2025-11-03 20:35:18.977691+02	t	19	264.00	184.80	f	t	t	t	2	t	t	t	t	\N	Casual comfortable clothing recommended	t	\N	Camera, comfortable walking shoes, sun protection	t	Regular sanitization, masks available, temperature checks	t	t	48	4.6	12	0
21	8	Icelandic Geothermal & Volcanic Landscape Adventure	icelandic-geothermal-volcanic-landscape-adventure	Discover the raw power of Iceland's geological forces through visits to active geothermal areas, volcanic sites, and unique landscapes found nowhere else on Earth. Learn about plate tectonics, volcanic activity, and renewable geothermal energy while soaking in natural hot springs, walking on glaciers, and witnessing the Northern Lights. This adventure combines education with unforgettable natural experiences.	Explore Iceland's unique geothermal wonders and volcanic landscapes on this geological adventure	195.00	136.50	EUR	540	13	t	24	{english,chinese,spanish}	f	t	t	2025-08-13 17:27:29.550601+03	2025-11-03 20:35:18.977691+02	t	17	234.00	163.80	f	t	t	t	2	f	t	t	f	\N	Casual comfortable clothing recommended	t	\N	Camera, comfortable walking shoes, sun protection	t	Regular sanitization, masks available, temperature checks	t	t	48	4.6	12	0
22	8	Stockholm Modern Design & Architecture Walking Tour	stockholm-modern-design-architecture-walking-tour	Explore Stockholm's reputation as a global design capital through this comprehensive walking tour of the city's most innovative architecture and design districts. Visit renowned design studios, meet local designers, explore modern architectural marvels, and understand how Swedish design principles influence everything from furniture to urban planning. Experience the intersection of functionality, beauty, and sustainability in Swedish design.	Discover Stockholm's cutting-edge design scene and architectural innovations	75.00	52.50	EUR	240	14	t	24	{english,chinese,spanish}	t	f	t	2025-06-27 17:27:29.558159+03	2025-11-03 20:35:18.977691+02	t	10	90.00	63.00	f	t	t	t	2	t	t	t	f	\N	Casual comfortable clothing recommended	t	\N	Camera, comfortable walking shoes, sun protection	t	Regular sanitization, masks available, temperature checks	t	t	48	4.6	12	0
\.


--
-- TOC entry 4196 (class 0 OID 27107)
-- Dependencies: 242
-- Data for Name: activity_add_ons; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activity_add_ons (id, activity_id, name, description, price, is_optional, order_index) FROM stdin;
1	1	Professional Photography	Professional photographer to capture your experience	35.00	t	0
2	1	Traditional Lunch	Authentic local cuisine lunch experience	25.00	t	1
3	1	Souvenir Package	Curated selection of local souvenirs and gifts	18.00	t	2
4	1	Transportation Upgrade	Private vehicle instead of group transportation	45.00	t	3
5	2	Professional Photography	Professional photographer to capture your experience	35.00	t	0
6	2	Traditional Lunch	Authentic local cuisine lunch experience	25.00	t	1
7	2	Souvenir Package	Curated selection of local souvenirs and gifts	18.00	t	2
8	2	Transportation Upgrade	Private vehicle instead of group transportation	45.00	t	3
9	3	Professional Photography	Professional photographer to capture your experience	35.00	t	0
10	3	Traditional Lunch	Authentic local cuisine lunch experience	25.00	t	1
11	3	Souvenir Package	Curated selection of local souvenirs and gifts	18.00	t	2
12	3	Transportation Upgrade	Private vehicle instead of group transportation	45.00	t	3
13	4	Professional Photography	Professional photographer to capture your experience	35.00	t	0
14	4	Traditional Lunch	Authentic local cuisine lunch experience	25.00	t	1
15	4	Souvenir Package	Curated selection of local souvenirs and gifts	18.00	t	2
16	4	Transportation Upgrade	Private vehicle instead of group transportation	45.00	t	3
17	5	Professional Photography	Professional photographer to capture your experience	35.00	t	0
18	5	Traditional Lunch	Authentic local cuisine lunch experience	25.00	t	1
19	5	Souvenir Package	Curated selection of local souvenirs and gifts	18.00	t	2
20	5	Transportation Upgrade	Private vehicle instead of group transportation	45.00	t	3
21	6	Professional Photography	Professional photographer to capture your experience	35.00	t	0
22	6	Traditional Lunch	Authentic local cuisine lunch experience	25.00	t	1
23	6	Souvenir Package	Curated selection of local souvenirs and gifts	18.00	t	2
24	6	Transportation Upgrade	Private vehicle instead of group transportation	45.00	t	3
\.


--
-- TOC entry 4221 (class 0 OID 27361)
-- Dependencies: 267
-- Data for Name: activity_addon_translations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activity_addon_translations (id, addon_id, language, name, description) FROM stdin;
\.


--
-- TOC entry 4179 (class 0 OID 26971)
-- Dependencies: 225
-- Data for Name: activity_categories; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activity_categories (activity_id, category_id) FROM stdin;
1	1
1	9
2	2
2	1
3	5
3	1
4	5
4	3
5	10
5	6
6	9
6	1
8	2
8	1
9	10
9	6
9	4
10	9
10	3
10	1
11	3
11	1
12	2
12	1
13	10
13	4
13	1
14	9
14	10
14	1
15	9
15	2
15	1
16	5
16	1
17	5
17	1
18	5
18	3
19	5
19	1
20	10
20	6
20	4
21	10
21	6
21	4
22	3
22	1
\.


--
-- TOC entry 4180 (class 0 OID 26986)
-- Dependencies: 226
-- Data for Name: activity_destinations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activity_destinations (activity_id, destination_id) FROM stdin;
1	1
2	2
3	7
4	8
5	9
6	3
8	5
9	19
10	1
11	18
12	2
13	4
14	6
15	3
16	9
17	10
18	8
19	7
20	12
21	11
22	7
\.


--
-- TOC entry 4215 (class 0 OID 27310)
-- Dependencies: 261
-- Data for Name: activity_faq_translations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activity_faq_translations (id, faq_id, language, question, answer) FROM stdin;
1	1	zh	参观长城需要多长时间？	整个行程大约8-9小时，包括往返交通时间。在长城停留约3-4小时。
2	2	zh	午餐包含什么？	正宗中式午餐包含多道传统菜肴，适合各种口味偏好。
3	3	zh	如果天气不好怎么办？	除非极端天气，否则行程照常进行。我们建议穿着合适的衣物。
4	1	es	¿Cuánto tiempo dura la visita a la Gran Muralla?	El tour completo dura aproximadamente 8-9 horas, incluyendo el tiempo de transporte. Permanecerás en la Gran Muralla por unas 3-4 horas.
5	2	es	¿Qué incluye el almuerzo?	El almuerzo chino auténtico incluye varios platos tradicionales que se adaptan a diferentes preferencias de sabor.
6	3	es	¿Qué pasa si el clima es malo?	El tour procede normalmente a menos que haya condiciones climáticas extremas. Recomendamos vestimenta apropiada.
7	1	fr	Combien de temps dure la visite de la Grande Muraille?	Le tour complet dure environ 8-9 heures, y compris le temps de transport. Vous resterez à la Grande Muraille pendant environ 3-4 heures.
8	2	fr	Qu'est-ce qui est inclus dans le déjeuner?	Le déjeuner chinois authentique comprend plusieurs plats traditionnels qui s'adaptent à différentes préférences gustatives.
9	3	fr	Que se passe-t-il si le temps est mauvais?	Le tour a lieu normalement sauf en cas de conditions météorologiques extrêmes. Nous recommandons des vêtements appropriés.
10	4	zh	我们会品尝多少种不同的食物？	您将品尝10-12种不同的传统上海小食和菜肴，包括小笼包、生煎包等当地特色。
11	5	zh	对食物过敏的人怎么办？	请提前告知我们您的过敏情况，我们会相应调整品尝选择。
12	6	zh	这个行程适合素食者吗？	是的，我们可以安排素食选择，但请在预订时告知我们。
13	4	es	¿Cuántos tipos diferentes de comida probaremos?	Probarás 10-12 tipos diferentes de comida tradicional de Shanghái, incluyendo xiaolongbao, shengjianbao y otras especialidades locales.
14	5	es	¿Qué pasa si tengo alergias alimentarias?	Por favor informa sobre tus alergias con anticipación y ajustaremos las opciones de degustación en consecuencia.
15	6	es	¿Es este tour adecuado para vegetarianos?	Sí, podemos proporcionar opciones vegetarianas, pero por favor infórmanos al momento de la reserva.
16	4	fr	Combien de types différents de nourriture goûterons-nous?	Vous goûterez 10-12 types différents de nourriture traditionnelle de Shanghai, y compris xiaolongbao, shengjianbao et d'autres spécialités locales.
17	5	fr	Que se passe-t-il si j'ai des allergies alimentaires?	Veuillez nous informer de vos allergies à l'avance et nous ajusterons les options de dégustation en conséquence.
18	6	fr	Ce tour convient-il aux végétariens?	Oui, nous pouvons fournir des options végétariennes, mais veuillez nous en informer lors de la réservation.
19	7	zh	这个项目需要什么先决条件吗？	不需要特殊先决条件，但对教育或学术研究的兴趣会让体验更有意义。
20	8	zh	我们会获得什么样的学习材料？	您将获得关于瑞典教育体系的综合资料包，包括统计数据、政策文件和研究报告。
21	9	zh	可以安排与特定专业的学生会面吗？	是的，如果提前请求，我们可以安排与您感兴趣领域的学生会面。
22	7	es	¿Se requieren prerrequisitos para este programa?	No se requieren prerrequisitos especiales, pero el interés en educación o investigación académica hará la experiencia más significativa.
23	8	es	¿Qué tipo de materiales de estudio recibiremos?	Recibirás un paquete integral de materiales sobre el sistema educativo sueco, incluyendo estadísticas, documentos de política e informes de investigación.
24	9	es	¿Se pueden organizar reuniones con estudiantes de campos específicos?	Sí, podemos organizar reuniones con estudiantes en tu área de interés si se solicita con anticipación.
25	7	fr	Y a-t-il des prérequis pour ce programme?	Aucun prérequis spécial n'est requis, mais un intérêt pour l'éducation ou la recherche académique rendra l'expérience plus significative.
26	8	fr	Quel type de matériaux d'étude recevrons-nous?	Vous recevrez un pack complet de matériaux sur le système éducatif suédois, incluant des statistiques, des documents de politique et des rapports de recherche.
27	9	fr	Peut-on organiser des rencontres avec des étudiants de domaines spécifiques?	Oui, nous pouvons organiser des rencontres avec des étudiants dans votre domaine d'intérêt si demandé à l'avance.
28	16	zh	参观兵马俑需要多长时间？	整个参观大约需要3-4小时，包括所有三个坑和博物馆展览。
29	17	zh	可以拍照吗？	大部分区域允许拍照，但请不要使用闪光灯。某些特殊展区可能禁止拍照。
30	18	zh	最佳参观时间是什么时候？	早上9-10点或下午2-3点人流较少，拍照和观看效果更好。
31	16	es	¿Cuánto tiempo toma visitar el Ejército de Terracota?	La visita completa toma aproximadamente 3-4 horas, incluyendo las tres fosas y las exhibiciones del museo.
32	17	es	¿Se permite tomar fotos?	La fotografía está permitida en la mayoría de las áreas, pero por favor no uses flash. Algunas áreas de exposición especiales pueden prohibir las fotos.
33	18	es	¿Cuál es el mejor momento para visitar?	Las mañanas de 9-10 AM o las tardes de 2-3 PM tienen menos multitudes, mejores oportunidades para fotos y visualización.
34	16	fr	Combien de temps faut-il pour visiter l'Armée de Terre Cuite?	La visite complète prend environ 3-4 heures, incluant les trois fosses et les expositions du musée.
35	17	fr	La photographie est-elle autorisée?	La photographie est autorisée dans la plupart des zones, mais veuillez ne pas utiliser le flash. Certaines zones d'exposition spéciales peuvent interdire les photos.
36	18	fr	Quel est le meilleur moment pour visiter?	Les matins de 9h-10h ou les après-midis de 14h-15h ont moins de foules, de meilleures opportunités de photos et de visualisation.
37	19	zh	我们会学习制作几道菜？	您将学习制作3-4道经典川菜，包括麻婆豆腐、宫保鸡丁和担担面。
38	20	zh	课程对初学者友好吗？	绝对的！我们的大师厨师会从基础技巧开始教学，适合所有技能水平。
39	21	zh	我能处理辣味吗？	我们会教您如何调节辣味水平，并可以根据您的耐受度调整菜肴。
40	19	es	¿Cuántos platos aprenderemos a preparar?	Aprenderás a preparar 3-4 platos clásicos de Sichuan, incluyendo Mapo Tofu, Pollo Kung Pao y Fideos Dan Dan.
41	20	es	¿Es la clase amigable para principiantes?	¡Absolutamente! Nuestros chefs maestros comienzan con técnicas básicas y son adecuados para todos los niveles de habilidad.
42	21	es	¿Podré manejar el nivel de picante?	Te enseñaremos cómo ajustar los niveles de picante y podemos adaptar los platos a tu tolerancia.
43	19	fr	Combien de plats apprendrons-nous à préparer?	Vous apprendrez à préparer 3-4 plats classiques du Sichuan, y compris Mapo Tofu, Poulet Kung Pao et Nouilles Dan Dan.
44	20	fr	Le cours est-il adapté aux débutants?	Absolument! Nos chefs maîtres commencent par des techniques de base et conviennent à tous les niveaux de compétence.
45	21	fr	Pourrai-je gérer le niveau d'épices?	Nous vous enseignerons comment ajuster les niveaux d'épices et pouvons adapter les plats à votre tolérance.
46	22	zh	我需要带什么摄影设备？	推荐使用单反或无反相机配长焦镜头。我们会提供详细设备清单。也有设备租赁选项。
47	23	zh	什么时候最适合拍摄北极光？	9月到3月是北极光季节，但天气条件会影响能见度。我们会根据预报调整行程。
48	24	zh	初学者可以参加吗？	绝对可以！我们的摄影师会提供从基础到高级的指导，适合所有技能水平。
49	22	es	¿Qué equipo fotográfico necesito traer?	Se recomienda una cámara DSLR o sin espejo con lentes teleobjetivo. Proporcionaremos una lista detallada de equipo. También hay opciones de alquiler disponibles.
50	23	es	¿Cuándo es el mejor momento para fotografiar auroras boreales?	De septiembre a marzo es la temporada de auroras boreales, pero las condiciones climáticas afectan la visibilidad. Ajustaremos el itinerario según las previsiones.
51	24	es	¿Pueden participar principiantes?	¡Absolutamente! Nuestros fotógrafos proporcionan orientación desde básica hasta avanzada, adecuada para todos los niveles de habilidad.
52	22	fr	Quel équipement photographique dois-je apporter?	Un appareil photo reflex ou sans miroir avec des objectifs téléobjectifs est recommandé. Nous fournirons une liste détaillée d'équipement. Des options de location sont également disponibles.
53	23	fr	Quand est le meilleur moment pour photographier les aurores boréales?	De septembre à mars est la saison des aurores boréales, mais les conditions météorologiques affectent la visibilité. Nous ajusterons l'itinéraire selon les prévisions.
54	24	fr	Les débutants peuvent-ils participer?	Absolument! Nos photographes fournissent des conseils de base à avancés, adaptés à tous les niveaux de compétence.
55	34	zh	我应该带什么摄影设备？	推荐携带单反或无反相机配多个镜头。三脚架对风景拍摄很有用。预订后我们会提供详细设备清单。
56	35	zh	能到达阿凡达电影拍摄地吗？	是的，我们会参观阿凡达电影的实际拍摄地，包括著名的'哈利路亚山'。大部分地点可通过缆车和电梯到达。
57	36	zh	什么时候最适合摄影？	清晨和傍晚光线最佳。山区天气变化快，我们会根据最佳条件调整时间安排。
58	34	es	¿Qué equipo fotográfico debo traer?	Se recomienda una cámara DSLR o sin espejo con múltiples lentes. Los trípodes son útiles para tomas paisajísticas. Proporcionaremos una lista detallada de equipo al reservar.
59	35	es	¿Son accesibles las locaciones de filmación de Avatar?	Sí, visitamos las locaciones reales usadas en la película Avatar, incluyendo las famosas 'Montañas Aleluya'. La mayoría de las locaciones son accesibles vía teleféricos y ascensores.
60	36	es	¿Cuál es el mejor momento para fotografiar?	La mañana temprano y el atardecer proporcionan la mejor iluminación. El clima puede cambiar rápidamente en las montañas, así que ajustaremos el horario para condiciones óptimas.
61	34	fr	Quel équipement photographique dois-je apporter?	Un appareil photo reflex ou sans miroir avec plusieurs objectifs est recommandé. Les trépieds sont utiles pour les prises de paysage. Nous fournirons une liste détaillée d'équipement lors de la réservation.
62	35	fr	Les lieux de tournage d'Avatar sont-ils accessibles?	Oui, nous visitons les lieux réels utilisés dans le film Avatar, y compris les fameuses 'Montagnes Alléluia'. La plupart des lieux sont accessibles via téléphériques et ascenseurs.
63	36	fr	Quel est le meilleur moment pour photographier?	Le matin tôt et la fin d'après-midi offrent le meilleur éclairage. Le temps peut changer rapidement en montagne, nous ajusterons donc le timing pour des conditions optimales.
64	10	zh	Do I need design experience?	No prior experience needed. The workshop is designed for all skill levels.
65	11	zh	What will I create in the workshop?	You'll create a small design piece following Danish design principles.
66	12	zh	Can I keep what I make?	Basic workshop piece is included, but premium materials require additional fee.
67	10	es	Do I need design experience?	No prior experience needed. The workshop is designed for all skill levels.
68	11	es	What will I create in the workshop?	You'll create a small design piece following Danish design principles.
69	12	es	Can I keep what I make?	Basic workshop piece is included, but premium materials require additional fee.
70	10	fr	Do I need design experience?	No prior experience needed. The workshop is designed for all skill levels.
71	11	fr	What will I create in the workshop?	You'll create a small design piece following Danish design principles.
72	12	fr	Can I keep what I make?	Basic workshop piece is included, but premium materials require additional fee.
73	40	zh	What type of modern art will we see?	You'll experience contemporary Chinese art, digital installations, sculpture, and multimedia works from both established and emerging artists.
74	41	zh	Can we meet local artists?	Yes, the tour includes visits to active artist studios where you can meet creators and learn about their work and creative processes.
75	42	zh	Is this suitable for art beginners?	Absolutely! Our expert guides provide context and interpretation that makes contemporary art accessible to all knowledge levels.
76	40	es	What type of modern art will we see?	You'll experience contemporary Chinese art, digital installations, sculpture, and multimedia works from both established and emerging artists.
77	41	es	Can we meet local artists?	Yes, the tour includes visits to active artist studios where you can meet creators and learn about their work and creative processes.
78	42	es	Is this suitable for art beginners?	Absolutely! Our expert guides provide context and interpretation that makes contemporary art accessible to all knowledge levels.
79	40	fr	What type of modern art will we see?	You'll experience contemporary Chinese art, digital installations, sculpture, and multimedia works from both established and emerging artists.
80	41	fr	Can we meet local artists?	Yes, the tour includes visits to active artist studios where you can meet creators and learn about their work and creative processes.
81	42	fr	Is this suitable for art beginners?	Absolutely! Our expert guides provide context and interpretation that makes contemporary art accessible to all knowledge levels.
82	31	zh	What types of startups will we visit?	We visit a diverse range of Finnish startups across tech, sustainability, gaming, and social innovation sectors.
83	32	zh	Will we get to pitch our own ideas?	Yes, there are optional pitch sessions where participants can present their ideas to Finnish entrepreneurs for feedback.
84	33	zh	Is this suitable for non-entrepreneurs?	Absolutely! The program is valuable for students, researchers, investors, and anyone interested in innovation ecosystems.
85	31	es	What types of startups will we visit?	We visit a diverse range of Finnish startups across tech, sustainability, gaming, and social innovation sectors.
86	32	es	Will we get to pitch our own ideas?	Yes, there are optional pitch sessions where participants can present their ideas to Finnish entrepreneurs for feedback.
87	33	es	Is this suitable for non-entrepreneurs?	Absolutely! The program is valuable for students, researchers, investors, and anyone interested in innovation ecosystems.
88	31	fr	What types of startups will we visit?	We visit a diverse range of Finnish startups across tech, sustainability, gaming, and social innovation sectors.
89	32	fr	Will we get to pitch our own ideas?	Yes, there are optional pitch sessions where participants can present their ideas to Finnish entrepreneurs for feedback.
90	33	fr	Is this suitable for non-entrepreneurs?	Absolutely! The program is valuable for students, researchers, investors, and anyone interested in innovation ecosystems.
\.


--
-- TOC entry 4186 (class 0 OID 27032)
-- Dependencies: 232
-- Data for Name: activity_faqs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activity_faqs (id, activity_id, question, answer, order_index) FROM stdin;
1	1	How long is the hike on the wall?	The typical walk is 1-2 hours depending on your fitness level and interest. You can walk at your own pace.	0
2	1	Is this tour suitable for children?	Yes, this tour is family-friendly. The cable car makes it accessible for most fitness levels.	1
3	1	What should I wear?	Comfortable walking shoes and weather-appropriate clothing. The wall can be windy and cooler than Beijing city.	2
4	2	How much food is included?	You'll taste 10-12 different items, enough for a full meal experience.	0
5	2	Are dietary restrictions accommodated?	We can accommodate most dietary restrictions with advance notice.	1
6	2	Is the tour conducted in English?	Yes, all tours are conducted in fluent English with cultural context provided.	2
7	3	Who is this tour suitable for?	Perfect for prospective students, educators, parents, and anyone interested in Nordic education.	0
8	3	Can I get university application advice?	Basic guidance is included, but detailed consultation requires separate arrangement.	1
9	3	Is the tour available in Chinese?	Yes, we offer tours in Mandarin Chinese for Chinese-speaking groups.	2
10	4	Do I need design experience?	No prior experience needed. The workshop is designed for all skill levels.	0
11	4	What will I create in the workshop?	You'll create a small design piece following Danish design principles.	1
12	4	Can I keep what I make?	Basic workshop piece is included, but premium materials require additional fee.	2
13	5	What if we don't see the Northern Lights?	We offer a return trip within 48 hours if no aurora is visible due to weather.	0
14	5	How cold does it get?	Temperatures can drop to -20°C. We provide all necessary arctic gear.	1
15	5	Is this suitable for children?	Recommended for ages 8+ due to late night timing and cold weather conditions.	2
16	6	How long do we spend at the site?	Approximately 4 hours exploring all pits and exhibitions with detailed explanations.	0
17	6	Can I take photos?	Photography is allowed in most areas, but flash photography is prohibited to preserve the artifacts.	1
18	6	Is the tour wheelchair accessible?	Yes, the site has wheelchair access and our guides can accommodate mobility needs.	2
19	8	How many dishes will we learn to prepare?	You will learn to prepare 3-4 classic Sichuan dishes, including Mapo Tofu, Kung Pao Chicken, and Dan Dan Noodles.	1
20	8	Is the class beginner-friendly?	Absolutely! Our master chefs start with basic techniques and are suitable for all skill levels.	2
21	8	Can I handle the spice level?	We'll teach you how to adjust spice levels and can adapt dishes to your tolerance.	3
22	20	What photography equipment do I need to bring?	A DSLR or mirrorless camera with telephoto lenses is recommended. We'll provide a detailed equipment list. Rental options are also available.	1
23	20	When is the best time to photograph Northern Lights?	September to March is Northern Lights season, but weather conditions affect visibility. We'll adjust the itinerary based on forecasts.	2
24	20	Can beginners participate?	Absolutely! Our photographers provide guidance from basic to advanced levels, suitable for all skill levels.	3
25	6	How long does it take to visit the Terracotta Army?	The complete visit takes approximately 3-4 hours, including all three pits and museum exhibitions.	1
26	6	Is photography allowed?	Photography is allowed in most areas, but please don't use flash. Some special exhibition areas may prohibit photos.	2
27	6	What's the best time to visit?	Mornings 9-10 AM or afternoons 2-3 PM have fewer crowds, better photo opportunities and viewing.	3
28	16	Are there any prerequisites for this program?	No special prerequisites are required, but interest in sustainability or academic research will make the experience more meaningful.	1
29	16	What kind of study materials will we receive?	You'll receive a comprehensive materials package about Norwegian sustainability programs, including statistics, policy documents and research reports.	2
30	16	Can meetings with students from specific fields be arranged?	Yes, we can arrange meetings with students in your area of interest if requested in advance.	3
31	17	What types of startups will we visit?	We visit a diverse range of Finnish startups across tech, sustainability, gaming, and social innovation sectors.	1
32	17	Will we get to pitch our own ideas?	Yes, there are optional pitch sessions where participants can present their ideas to Finnish entrepreneurs for feedback.	2
33	17	Is this suitable for non-entrepreneurs?	Absolutely! The program is valuable for students, researchers, investors, and anyone interested in innovation ecosystems.	3
34	9	What photography equipment should I bring?	A DSLR or mirrorless camera with multiple lenses is recommended. Tripods are useful for landscape shots. We'll provide a detailed equipment list upon booking.	1
35	9	Are the Avatar filming locations accessible?	Yes, we visit the actual locations used in the Avatar movie, including the famous 'Hallelujah Mountains'. Most locations are accessible via cable cars and elevators.	2
36	9	What's the best time for photography?	Early morning and late afternoon provide the best lighting. Weather can change quickly in the mountains, so we'll adjust timing for optimal conditions.	3
37	10	Which temples will we visit?	We visit ancient temples including the Temple of Heaven and Lama Temple, each showcasing different aspects of Chinese religious and architectural traditions.	1
38	10	What traditional arts will we experience?	Activities include calligraphy, paper cutting, traditional painting, and seal carving. All skill levels are welcome with expert instruction.	2
39	10	Is photography allowed in temples?	Photography rules vary by location. Most areas allow photos, but some sacred spaces may restrict them. Your guide will inform you at each location.	3
40	11	What type of modern art will we see?	You'll experience contemporary Chinese art, digital installations, sculpture, and multimedia works from both established and emerging artists.	1
41	11	Can we meet local artists?	Yes, the tour includes visits to active artist studios where you can meet creators and learn about their work and creative processes.	2
42	11	Is this suitable for art beginners?	Absolutely! Our expert guides provide context and interpretation that makes contemporary art accessible to all knowledge levels.	3
43	12	How many different foods will we try?	You'll sample 8-10 different street food specialties including xiaolongbao, jianbing, scallion pancakes, and seasonal local favorites.	1
44	12	Is the street food safe to eat?	Yes, we only visit vendors with high standards and good reputations. Our guide will provide food safety tips and choose the best options.	2
45	12	What if I have dietary restrictions?	Please inform us of any allergies or dietary needs in advance. We can accommodate most restrictions with alternative tastings.	3
46	13	How long is the bamboo rafting experience?	The rafting journey lasts approximately 2-3 hours, covering the most scenic sections of the Li River with karst mountain landscapes.	1
47	13	Is bamboo rafting safe?	Yes, bamboo rafting is very safe. All rafts are inspected regularly, life jackets are provided, and experienced guides accompany each raft.	2
48	13	What should I bring?	Bring sun protection, waterproof bags for electronics, comfortable clothing, and non-slip shoes. Camera for capturing the stunning scenery!	3
49	14	What cultural sites will we visit?	We'll visit key West Lake landmarks including Leifeng Pagoda, Su Causeway, and Lingyin Temple, each with rich cultural significance.	1
50	14	How much walking is involved?	The walk is moderate, about 3-4 kilometers at a leisurely pace with frequent stops. Most paths are flat and well-maintained.	2
51	14	What legends will we learn about?	You'll hear famous stories like the Legend of the White Snake and other traditional tales that have shaped West Lake's cultural identity.	3
52	15	What aspects of Silk Road history will we explore?	We'll cover Xi'an's role as the eastern terminus of the Silk Road, trade routes, cultural exchange, and the city's multicultural heritage.	1
53	15	What food will we taste in the Muslim Quarter?	You'll try traditional Hui Muslim cuisine including roujiamo (Chinese hamburger), yangrou paomo (bread and mutton soup), and local sweets.	2
54	15	Are there any cultural sensitivities to be aware of?	We'll provide cultural guidance for visiting the Muslim Quarter, including appropriate behavior in religious areas and respectful interaction with locals.	3
55	18	What level of Danish will be taught?	We focus on practical conversational Danish for travelers, including greetings, ordering food, asking directions, and basic social interactions.	1
56	18	Will we interact with local Danes?	Yes, the experience includes structured conversations with native speakers in casual settings like cafes or community centers.	2
57	18	What Danish cultural aspects will we learn?	You'll learn about hygge philosophy, Danish social customs, work-life balance culture, and practical etiquette for interacting with Danes.	3
58	19	What teaching methods will we observe?	You'll see progressive Swedish education including collaborative learning, student-centered approaches, critical thinking development, and innovative assessment methods.	1
59	19	Can we participate in classes?	Depending on school arrangements, you may observe classes and participate in some educational activities with students and teachers.	2
60	19	Is this suitable for non-educators?	Yes, while designed for educators, the tour is valuable for anyone interested in progressive education, child development, or Nordic social systems.	3
61	21	How close can we get to volcanic activity?	We visit safe viewing areas of active geothermal sites and dormant volcanic formations. All locations are assessed for safety by our expert guides.	1
62	21	What should I wear for this adventure?	Warm, waterproof clothing and sturdy hiking boots are essential. We'll provide detailed packing recommendations based on current conditions.	2
63	21	Is this experience suitable for beginners?	Yes, no special geological knowledge is required. Our expert guides explain everything from basics to advanced concepts in an accessible way.	3
64	22	What architectural styles will we explore?	We'll see Swedish modernism, functionalism, contemporary Scandinavian design, and innovative sustainable architecture from the 20th and 21st centuries.	1
65	22	Will we visit design studios?	Yes, the tour includes visits to active design studios and showrooms where you can see contemporary Swedish design in development.	2
66	22	How much walking is involved?	The tour covers about 4-5 kilometers over 3 hours with regular stops. Most walking is on flat city streets with some stairs in buildings.	3
\.


--
-- TOC entry 4211 (class 0 OID 27276)
-- Dependencies: 257
-- Data for Name: activity_highlight_translations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activity_highlight_translations (id, highlight_id, language, text) FROM stdin;
1	1	zh	游览世界七大奇迹之一的万里长城
2	2	zh	专业当地导游讲解历史文化
3	3	zh	享用正宗中式午餐
4	4	zh	包含往返交通和缆车票
5	5	zh	参观保存完好的慕田峪段
6	1	es	Visita una de las Siete Maravillas del Mundo
7	2	es	Guía local experto con conocimiento histórico
8	3	es	Almuerzo chino auténtico incluido
9	4	es	Transporte de ida y vuelta incluido
10	5	es	Acceso a la sección Mutianyu bien conservada
11	1	fr	Visitez l'une des Sept Merveilles du Monde
12	2	fr	Guide local expert avec connaissances historiques
13	3	fr	Déjeuner chinois authentique inclus
14	4	fr	Transport aller-retour inclus
15	5	fr	Accès à la section Mutianyu bien préservée
16	6	zh	品尝正宗小笼包和生煎包
17	7	zh	探索当地人常去的湿货市场
18	8	zh	发现隐藏的美食宝藏
19	9	zh	学习上海烹饪传统和历史
20	10	zh	品尝多种街头小食
21	6	es	Degusta auténticos xiaolongbao y shengjianbao
22	7	es	Explora mercados húmedos frecuentados por locales
23	8	es	Descubre joyas gastronómicas ocultas
24	9	es	Aprende sobre tradiciones culinarias de Shanghái
25	10	es	Prueba variedad de comida callejera
26	6	fr	Dégustez d'authentiques xiaolongbao et shengjianbao
27	7	fr	Explorez les marchés fréquentés par les locaux
28	8	fr	Découvrez des trésors gastronomiques cachés
29	9	fr	Apprenez les traditions culinaires de Shanghai
30	10	fr	Goûtez une variété de street food
31	37	zh	向认证川菜大师学习烹饪
32	38	zh	制作经典川菜如麻婆豆腐
33	39	zh	学习正宗'麻辣'调味技巧
34	40	zh	参观当地香料市场
35	41	zh	获得正宗川菜食谱
36	37	es	Aprende de chefs maestros certificados de Sichuan
37	38	es	Prepara clásicos de Sichuan como Mapo Tofu
38	39	es	Domina técnicas auténticas de condimentado 'mala'
39	40	es	Visita mercados locales de especias
40	41	es	Recibe recetas auténticas de Sichuan
41	37	fr	Apprenez auprès de chefs maîtres certifiés du Sichuan
42	38	fr	Préparez des classiques du Sichuan comme le Mapo Tofu
43	39	fr	Maîtrisez les techniques d'assaisonnement 'mala' authentiques
44	40	fr	Visitez les marchés locaux d'épices
45	41	fr	Recevez des recettes authentiques du Sichuan
46	11	zh	参观斯德哥尔摩大学现代化校园
47	12	zh	与国际学生和教授互动
48	13	zh	了解瑞典教育创新方法
49	14	zh	探索北欧教育哲学
50	15	zh	获得教育体系深入洞察
51	11	es	Visita el moderno campus de la Universidad de Estocolmo
52	12	es	Interactúa con estudiantes internacionales y profesores
53	13	es	Aprende sobre enfoques educativos innovadores suecos
54	14	es	Explora la filosofía educativa nórdica
55	15	es	Obtén perspectivas profundas del sistema educativo
56	11	fr	Visitez le campus moderne de l'Université de Stockholm
57	12	fr	Interagissez avec des étudiants internationaux et des professeurs
58	13	fr	Apprenez les approches éducatives innovantes suédoises
59	14	fr	Explorez la philosophie éducative nordique
60	15	fr	Obtenez des perspectives profondes du système éducatif
61	26	zh	参观世界著名的兵马俑博物馆
62	27	zh	观看数千个独特的陶制战士
63	28	zh	了解秦始皇和中国统一
64	29	zh	探索考古发现过程
65	30	zh	体验中国古代历史文化
66	26	es	Visita el mundialmente famoso Museo del Ejército de Terracota
67	27	es	Observa miles de guerreros de terracota únicos
68	28	es	Aprende sobre el Emperador Qin Shi Huang y la unificación china
69	29	es	Explora el proceso de descubrimiento arqueológico
70	30	es	Experimenta la historia y cultura china antigua
71	26	fr	Visitez le Musée de l'Armée de Terre Cuite mondialement célèbre
72	27	fr	Observez des milliers de guerriers en terre cuite uniques
73	28	fr	Apprenez sur l'Empereur Qin Shi Huang et l'unification chinoise
74	29	fr	Explorez le processus de découverte archéologique
75	30	fr	Vivez l'histoire et la culture chinoises anciennes
76	109	zh	拍摄壮观的挪威峡湾景观
77	110	zh	观察和拍摄北极野生动物
78	111	zh	向专业摄影师学习技巧
79	112	zh	体验午夜太阳或北极光
80	113	zh	掌握极端天气摄影技术
81	109	es	Fotografía paisajes espectaculares de fiordos noruegos
82	110	es	Observa y fotografía vida silvestre ártica
83	111	es	Aprende técnicas de fotógrafos profesionales
84	112	es	Experimenta el sol de medianoche o auroras boreales
85	113	es	Domina técnicas de fotografía en clima extremo
86	109	fr	Photographiez des paysages spectaculaires de fjords norvégiens
87	110	fr	Observez et photographiez la faune arctique
88	111	fr	Apprenez des techniques de photographes professionnels
89	112	fr	Vivez le soleil de minuit ou les aurores boréales
90	113	fr	Maîtrisez les techniques de photographie par temps extrême
91	42	zh	参观当地香料市场
92	42	es	Visita mercados locales de especias
93	42	fr	Visitez les marchés locaux d'épices
94	114	zh	体验午夜太阳或北极光
95	114	es	Experimenta el sol de medianoche o auroras boreales
96	114	fr	Vivez le soleil de minuit ou les aurores boréales
97	21	zh	专业北极光预测和拍摄指导
98	22	zh	体验萨米族传统文化和生活方式
99	23	zh	参观驯鹿农场和了解放牧传统
100	24	zh	学习北极生存技巧和文化知识
101	25	zh	品尝地道的北极地区美食
102	21	es	Predicción profesional de auroras boreales y guía fotográfica
103	22	es	Experimenta la cultura tradicional Sami y estilo de vida
104	23	es	Visita granjas de renos y aprende tradiciones de pastoreo
105	24	es	Aprende técnicas de supervivencia ártica y conocimiento cultural
106	25	es	Degusta auténtica cocina de la región ártica
107	21	fr	Prédiction professionnelle d'aurores boréales et guide photographique
108	22	fr	Vivez la culture traditionnelle Sami et le mode de vie
109	23	fr	Visitez les fermes de rennes et apprenez les traditions d'élevage
110	24	fr	Apprenez les techniques de survie arctique et connaissances culturelles
111	25	fr	Dégustez l'authentique cuisine de la région arctique
112	43	zh	拍摄阿凡达电影取景地的真实场景
113	44	zh	乘坐百龙天梯欣赏垂直峰林
114	45	zh	体验世界最长玻璃栈道的刺激
115	46	zh	专业摄影师传授峰林拍摄技巧
116	47	zh	探索袁家界和天门山核心景区
117	48	zh	捕捉云海和峰林的绝美瞬间
118	43	es	Fotografía escenas reales de las locaciones de la película Avatar
119	44	es	Toma el Ascensor Bailong para admirar el bosque de picos verticales
120	45	es	Experimenta la emoción del sendero de cristal más largo del mundo
121	46	es	Fotógrafos profesionales enseñan técnicas de fotografía de bosques de picos
122	47	es	Explora las áreas centrales de Yuanjiajie y Tianmen
123	48	es	Captura momentos perfectos del mar de nubes y bosques de picos
124	43	fr	Photographiez des scènes réelles des lieux de tournage du film Avatar
125	44	fr	Prenez l'Ascenseur Bailong pour admirer la forêt de pics verticaux
126	45	fr	Vivez l'excitation du sentier de verre le plus long du monde
127	46	fr	Des photographes professionnels enseignent les techniques de photographie de forêts de pics
128	47	fr	Explorez les zones centrales de Yuanjiajie et Tianmen
129	48	fr	Capturez des moments parfaits de mer de nuages et forêts de pics
130	49	zh	参访天坛、雍和宫等著名古寺
131	50	zh	学习中国书法和传统绘画技巧
132	51	zh	体验剪纸、篆刻等传统手工艺
133	52	zh	与资深艺术家面对面交流学习
134	53	zh	了解佛教文化和寺庙建筑艺术
135	54	zh	参加传统茶艺仪式体验
136	49	es	Visita famosos templos antiguos como Templo del Cielo y Templo Lama
137	50	es	Aprende caligrafía china y técnicas de pintura tradicional
138	51	es	Experimenta artesanías tradicionales como papel cortado y grabado de sellos
139	52	es	Intercambia y aprende cara a cara con artistas experimentados
140	53	es	Comprende la cultura budista y arte arquitectónico de templos
141	54	es	Participa en experiencia de ceremonia de té tradicional
142	49	fr	Visitez des temples anciens célèbres comme le Temple du Ciel et Temple Lama
143	50	fr	Apprenez la calligraphie chinoise et techniques de peinture traditionnelle
144	51	fr	Vivez des artisanats traditionnels comme découpage de papier et gravure de sceaux
145	52	fr	Échangez et apprenez face à face avec des artistes expérimentés
146	53	fr	Comprenez la culture bouddhiste et l'art architectural des temples
147	54	fr	Participez à l'expérience de cérémonie de thé traditionnelle
148	16	zh	探访世界知名的哥本哈根设计学院
149	17	zh	学习丹麦简约主义设计哲学
150	18	zh	与专业设计师和教授互动交流
151	19	zh	参观现代设计工作室和展厅
152	20	zh	了解可持续设计的创新理念
153	16	es	Visita la mundialmente famosa Academia de Diseño de Copenhague
154	17	es	Aprende filosofía del diseño minimalista danés
155	18	es	Interactúa e intercambia con diseñadores profesionales y profesores
156	19	es	Visita estudios de diseño moderno y salas de exhibición
157	20	es	Comprende conceptos innovadores de diseño sostenible
158	16	fr	Visitez l'Académie de Design de Copenhague mondialement célèbre
159	17	fr	Apprenez la philosophie du design minimaliste danois
160	18	fr	Interagissez et échangez avec des designers professionnels et professeurs
161	19	fr	Visitez des studios de design moderne et salles d'exposition
162	20	fr	Comprenez les concepts innovants de design durable
163	55	zh	参观广州知名现代艺术画廊
164	56	zh	探索红砖厂等创意文化园区
165	57	zh	与当地艺术家和设计师交流
166	58	zh	了解岭南文化与现代艺术融合
167	59	zh	体验广州创新创业氛围
168	60	zh	参观艺术家工作室和展览空间
169	55	es	Visita galerías de arte moderno famosas de Guangzhou
170	56	es	Explora parques culturales creativos como Red Brick Factory
171	57	es	Intercambia con artistas locales y diseñadores
172	58	es	Comprende la fusión de cultura Lingnan con arte moderno
173	59	es	Experimenta la atmósfera de innovación y emprendimiento de Guangzhou
174	60	es	Visita estudios de artistas y espacios de exhibición
175	55	fr	Visitez des galeries d'art moderne célèbres de Guangzhou
176	56	fr	Explorez des parcs culturels créatifs comme Red Brick Factory
177	57	fr	Échangez avec des artistes locaux et designers
178	58	fr	Comprenez la fusion de la culture Lingnan avec l'art moderne
179	59	fr	Vivez l'atmosphère d'innovation et d'entrepreneuriat de Guangzhou
180	60	fr	Visitez des studios d'artistes et espaces d'exposition
181	91	zh	参访芬兰顶级创新中心和孵化器
182	92	zh	与成功创业者和投资人面对面交流
183	93	zh	学习芬兰创新方法论和商业模式
184	94	zh	了解北欧创业生态系统的独特优势
185	95	zh	参观知名科技公司和研发中心
186	96	zh	体验芬兰创新文化和工作理念
187	91	es	Visita centros de innovación e incubadoras top de Finlandia
188	92	es	Intercambia cara a cara con emprendedores exitosos e inversionistas
189	93	es	Aprende metodologías de innovación finlandesas y modelos de negocio
190	94	es	Comprende ventajas únicas del ecosistema emprendedor nórdico
191	95	es	Visita empresas tecnológicas famosas y centros de I+D
192	96	es	Experimenta cultura de innovación finlandesa y conceptos de trabajo
193	91	fr	Visitez des centres d'innovation et incubateurs top de Finlande
194	92	fr	Échangez face à face avec des entrepreneurs réussis et investisseurs
195	93	fr	Apprenez les méthodologies d'innovation finlandaises et modèles d'affaires
196	94	fr	Comprenez les avantages uniques de l'écosystème entrepreneurial nordique
197	95	fr	Visitez des entreprises technologiques célèbres et centres de R&D
198	96	fr	Vivez la culture d'innovation finlandaise et concepts de travail
\.


--
-- TOC entry 4182 (class 0 OID 27002)
-- Dependencies: 228
-- Data for Name: activity_highlights; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activity_highlights (id, activity_id, text, order_index) FROM stdin;
1	1	Walk on the UNESCO World Heritage Great Wall	0
2	1	Private guide with expert historical knowledge	1
3	1	Scenic Mutianyu section with mountain views	2
4	1	Traditional Chinese lunch included	3
5	1	Round-trip transportation from Beijing	4
6	2	Authentic xiaolongbao at a century-old restaurant	0
7	2	Local wet market exploration with guide	1
8	2	Traditional shengjianbao from street vendors	2
9	2	Hidden food alleys off the tourist path	3
10	2	Cultural insights into Shanghai's food history	4
11	3	Guided tour of Stockholm University campus	0
12	3	Meet with international students and professors	1
13	3	Learn about Swedish higher education system	2
14	3	Interactive session on Nordic teaching methods	3
15	3	Campus library and research facility visits	4
16	4	Danish Design Academy campus tour	0
17	4	Hands-on design workshop with professionals	1
18	4	Meet with successful Danish designers	2
19	4	Learn about hygge and Danish design philosophy	3
20	4	Visit to iconic design studios and showrooms	4
21	5	Professional Northern Lights hunting with expert guide	0
22	5	Traditional Sami cultural presentation	1
23	5	Reindeer stew dinner around campfire	2
24	5	Arctic clothing and gear provided	3
25	5	Professional aurora photography tips	4
26	6	Expert archaeological guide with historical insights	0
27	6	Visit all three excavation pits	1
28	6	Bronze Chariot and Horse Exhibition	2
29	6	Latest archaeological discoveries explained	3
30	6	Qin Dynasty history and cultural significance	4
37	8	Professional cooking class with certified Sichuan chefs	0
38	8	Market visit to source authentic ingredients	1
39	8	Learn 5 traditional Sichuan dishes	2
40	8	Understand the science behind 'mala' flavor profile	3
41	8	Take home recipe book and spice samples	4
42	8	Small group size (max 8 participants)	5
43	9	Professional photography guide and instruction	0
44	9	Access to exclusive viewpoints and hidden locations	1
45	9	Golden hour and blue hour shooting sessions	2
46	9	Advanced landscape photography techniques	3
47	9	Glass bridge and cable car experiences	4
48	9	Photo editing workshop and portfolio review	5
49	10	Temple of Heaven and Lama Temple visits	0
50	10	Traditional calligraphy and paper cutting workshops	1
51	10	Meet with master craftsmen and artists	2
52	10	Authentic Chinese tea ceremony experience	3
53	10	Feng shui and traditional philosophy insights	4
54	10	Take home your own artistic creations	5
55	11	Contemporary art galleries and exhibitions	0
56	11	Artist studio visits and meet-and-greets	1
57	11	Innovative architecture and urban planning tour	2
58	11	Local creative community insights	3
59	11	Traditional meets modern cultural analysis	4
60	11	Photography opportunities in artistic spaces	5
61	12	Visit 4-5 different night markets and food streets	0
62	12	Sample 15+ different local street foods	1
63	12	Learn Shanghai food history and culture	2
64	12	Meet local vendors and food artisans	3
65	12	Navigate like a local with insider tips	4
66	12	Vegetarian and dietary options available	5
67	13	Traditional bamboo raft experience on Li River	0
68	13	Stunning karst mountain scenery and photo opportunities	1
69	13	Visit authentic fishing villages	2
70	13	Try traditional cormorant fishing techniques	3
71	13	Countryside lunch with local family	4
72	13	Learn about rural Chinese customs and traditions	5
73	14	UNESCO World Heritage West Lake exploration	0
74	14	Historic temples and pagodas visits	1
75	14	Traditional Chinese garden design insights	2
76	14	Poetry and literature associated with West Lake	3
77	14	Ancient causeway walks and scenic viewpoints	4
78	14	Tea plantation visit and Dragon Well tea tasting	5
79	15	Historic Muslim Quarter and Great Mosque exploration	0
80	15	Authentic Halal Chinese cuisine sampling	1
81	15	Silk Road history and cultural exchange insights	2
82	15	Traditional craft workshops and demonstrations	3
83	15	Multicultural heritage understanding	4
84	15	Street food tour through bustling bazaars	5
85	16	University of Oslo campus tour and facilities	0
86	16	Meet professors and researchers in sustainability	1
87	16	Hands-on workshops in renewable energy technology	2
88	16	Environmental policy and climate action seminars	3
89	16	Visit to green technology laboratories	4
90	16	Student exchange program information sessions	5
91	17	Visit to major Finnish tech companies and startups	0
92	17	Meet successful entrepreneurs and innovators	1
93	17	Innovation methodology workshops	2
94	17	Finnish education system insights	3
95	17	Nordic work culture and innovation environment	4
96	17	Networking opportunities with local professionals	5
97	18	Intensive Danish language classes with native speakers	0
98	18	Cultural immersion with local families	1
99	18	Visit Danish cultural institutions and museums	2
100	18	Practice language skills in real situations	3
101	18	Learn about hygge and Danish lifestyle	4
102	18	Cultural workshops and traditional activities	5
103	19	Visit Swedish schools and observe classes	0
104	19	Meet education experts and innovative teachers	1
105	19	Learn Swedish pedagogical methods and philosophy	2
106	19	Educational technology and digital learning insights	3
107	19	Inclusive education and student welfare systems	4
108	19	Educational policy and system design workshops	5
109	20	Professional wildlife photography instruction	0
110	20	Boat expedition through dramatic Norwegian fjords	1
111	20	Arctic wildlife spotting and photography	2
112	20	Northern lights or midnight sun photography	3
113	20	Extreme weather photography techniques	4
114	20	Post-processing workshop and portfolio review	5
115	21	Active geothermal areas and hot springs	0
116	21	Volcanic landscape exploration and education	1
117	21	Glacier walking and ice cave experiences	2
118	21	Northern Lights viewing (seasonal)	3
119	21	Renewable energy facility visits	4
120	21	Geological phenomena and plate tectonics insights	5
121	22	Modern architecture and urban design exploration	0
122	22	Visit renowned Swedish design studios	1
123	22	Meet local designers and architects	2
124	22	Swedish design philosophy and principles	3
125	22	Sustainable urban planning examples	4
126	22	Design shopping districts and showrooms	5
\.


--
-- TOC entry 4178 (class 0 OID 26957)
-- Dependencies: 224
-- Data for Name: activity_images; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activity_images (id, activity_id, url, alt_text, caption, is_primary, is_hero, order_index) FROM stdin;
1	1	https://picsum.photos/seed/great-wall-private-tour-beijing-0/800/600	Great Wall of China Private Day Tour with Lunch - Image 1	\N	t	t	0
2	1	https://picsum.photos/seed/great-wall-private-tour-beijing-1/800/600	Great Wall of China Private Day Tour with Lunch - Image 2	\N	f	f	1
3	1	https://picsum.photos/seed/great-wall-private-tour-beijing-2/800/600	Great Wall of China Private Day Tour with Lunch - Image 3	\N	f	f	2
4	1	https://picsum.photos/seed/great-wall-private-tour-beijing-3/800/600	Great Wall of China Private Day Tour with Lunch - Image 4	\N	f	f	3
5	1	https://picsum.photos/seed/great-wall-private-tour-beijing-4/800/600	Great Wall of China Private Day Tour with Lunch - Image 5	\N	f	f	4
27	4	https://picsum.photos/seed/copenhagen-design-academy-workshop-4/800/600	Copenhagen Design Academy & Danish Design Philosophy Workshop - Image 5	\N	f	f	4
28	4	https://picsum.photos/seed/copenhagen-design-academy-workshop-5/800/600	Copenhagen Design Academy & Danish Design Philosophy Workshop - Image 6	\N	f	f	5
29	4	https://picsum.photos/seed/copenhagen-design-academy-workshop-6/800/600	Copenhagen Design Academy & Danish Design Philosophy Workshop - Image 7	\N	f	f	6
30	5	https://picsum.photos/seed/oslo-northern-lights-arctic-culture-0/800/600	Northern Lights Chase & Arctic Culture Experience - Image 1	\N	t	t	0
31	5	https://picsum.photos/seed/oslo-northern-lights-arctic-culture-1/800/600	Northern Lights Chase & Arctic Culture Experience - Image 2	\N	f	f	1
32	5	https://picsum.photos/seed/oslo-northern-lights-arctic-culture-2/800/600	Northern Lights Chase & Arctic Culture Experience - Image 3	\N	f	f	2
33	5	https://picsum.photos/seed/oslo-northern-lights-arctic-culture-3/800/600	Northern Lights Chase & Arctic Culture Experience - Image 4	\N	f	f	3
34	5	https://picsum.photos/seed/oslo-northern-lights-arctic-culture-4/800/600	Northern Lights Chase & Arctic Culture Experience - Image 5	\N	f	f	4
35	5	https://picsum.photos/seed/oslo-northern-lights-arctic-culture-5/800/600	Northern Lights Chase & Arctic Culture Experience - Image 6	\N	f	f	5
36	6	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-0/800/600	Xi'an Terracotta Army Discovery Tour with Ancient History - Image 1	\N	t	t	0
37	6	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-1/800/600	Xi'an Terracotta Army Discovery Tour with Ancient History - Image 2	\N	f	f	1
38	6	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-2/800/600	Xi'an Terracotta Army Discovery Tour with Ancient History - Image 3	\N	f	f	2
39	6	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-3/800/600	Xi'an Terracotta Army Discovery Tour with Ancient History - Image 4	\N	f	f	3
40	6	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-4/800/600	Xi'an Terracotta Army Discovery Tour with Ancient History - Image 5	\N	f	f	4
41	6	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-5/800/600	Xi'an Terracotta Army Discovery Tour with Ancient History - Image 6	\N	f	f	5
42	6	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-6/800/600	Xi'an Terracotta Army Discovery Tour with Ancient History - Image 7	\N	f	f	6
78	12	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-image-5/800/600	Shanghai Street Food & Night Market Adventure - Image 6	\N	f	f	5
79	13	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-image-0/800/600	Guilin Li River Bamboo Rafting & Countryside - Image 1	\N	t	t	0
80	13	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-image-1/800/600	Guilin Li River Bamboo Rafting & Countryside - Image 2	\N	f	f	1
81	13	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-image-2/800/600	Guilin Li River Bamboo Rafting & Countryside - Image 3	\N	f	f	2
82	13	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-image-3/800/600	Guilin Li River Bamboo Rafting & Countryside - Image 4	\N	f	f	3
83	13	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-image-4/800/600	Guilin Li River Bamboo Rafting & Countryside - Image 5	\N	f	f	4
84	13	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-image-5/800/600	Guilin Li River Bamboo Rafting & Countryside - Image 6	\N	f	f	5
85	14	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-image-0/800/600	Hangzhou West Lake Cultural Heritage Walk - Image 1	\N	t	t	0
86	14	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-image-1/800/600	Hangzhou West Lake Cultural Heritage Walk - Image 2	\N	f	f	1
87	14	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-image-2/800/600	Hangzhou West Lake Cultural Heritage Walk - Image 3	\N	f	f	2
88	14	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-image-3/800/600	Hangzhou West Lake Cultural Heritage Walk - Image 4	\N	f	f	3
89	14	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-image-4/800/600	Hangzhou West Lake Cultural Heritage Walk - Image 5	\N	f	f	4
90	14	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-image-5/800/600	Hangzhou West Lake Cultural Heritage Walk - Image 6	\N	f	f	5
91	15	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-image-0/800/600	Xi'an Silk Road History & Muslim Quarter Experience - Image 1	\N	t	t	0
92	15	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-image-1/800/600	Xi'an Silk Road History & Muslim Quarter Experience - Image 2	\N	f	f	1
93	15	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-image-2/800/600	Xi'an Silk Road History & Muslim Quarter Experience - Image 3	\N	f	f	2
94	15	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-image-3/800/600	Xi'an Silk Road History & Muslim Quarter Experience - Image 4	\N	f	f	3
95	15	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-image-4/800/600	Xi'an Silk Road History & Muslim Quarter Experience - Image 5	\N	f	f	4
6	1	https://picsum.photos/seed/great-wall-private-tour-beijing-5/800/600	Great Wall of China Private Day Tour with Lunch - Image 6	\N	f	f	5
7	1	https://picsum.photos/seed/great-wall-private-tour-beijing-6/800/600	Great Wall of China Private Day Tour with Lunch - Image 7	\N	f	f	6
8	2	https://picsum.photos/seed/shanghai-food-tour-street-food-0/800/600	Shanghai Food Tour: Local Street Food and Hidden Gems - Image 1	\N	t	t	0
9	2	https://picsum.photos/seed/shanghai-food-tour-street-food-1/800/600	Shanghai Food Tour: Local Street Food and Hidden Gems - Image 2	\N	f	f	1
10	2	https://picsum.photos/seed/shanghai-food-tour-street-food-2/800/600	Shanghai Food Tour: Local Street Food and Hidden Gems - Image 3	\N	f	f	2
11	2	https://picsum.photos/seed/shanghai-food-tour-street-food-3/800/600	Shanghai Food Tour: Local Street Food and Hidden Gems - Image 4	\N	f	f	3
12	2	https://picsum.photos/seed/shanghai-food-tour-street-food-4/800/600	Shanghai Food Tour: Local Street Food and Hidden Gems - Image 5	\N	f	f	4
96	15	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-image-5/800/600	Xi'an Silk Road History & Muslim Quarter Experience - Image 6	\N	f	f	5
97	16	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-image-0/800/600	University of Oslo Sustainability & Green Technology Study Program - Image 1	\N	t	t	0
98	16	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-image-1/800/600	University of Oslo Sustainability & Green Technology Study Program - Image 2	\N	f	f	1
99	16	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-image-2/800/600	University of Oslo Sustainability & Green Technology Study Program - Image 3	\N	f	f	2
100	16	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-image-3/800/600	University of Oslo Sustainability & Green Technology Study Program - Image 4	\N	f	f	3
101	16	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-image-4/800/600	University of Oslo Sustainability & Green Technology Study Program - Image 5	\N	f	f	4
102	16	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-image-5/800/600	University of Oslo Sustainability & Green Technology Study Program - Image 6	\N	f	f	5
103	17	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-image-0/800/600	Finnish Innovation Hub & Startup Ecosystem Study Tour - Image 1	\N	t	t	0
104	17	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-image-1/800/600	Finnish Innovation Hub & Startup Ecosystem Study Tour - Image 2	\N	f	f	1
105	17	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-image-2/800/600	Finnish Innovation Hub & Startup Ecosystem Study Tour - Image 3	\N	f	f	2
106	17	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-image-3/800/600	Finnish Innovation Hub & Startup Ecosystem Study Tour - Image 4	\N	f	f	3
107	17	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-image-4/800/600	Finnish Innovation Hub & Startup Ecosystem Study Tour - Image 5	\N	f	f	4
108	17	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-image-5/800/600	Finnish Innovation Hub & Startup Ecosystem Study Tour - Image 6	\N	f	f	5
109	18	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-image-0/800/600	Danish Language & Culture Immersion Experience - Image 1	\N	t	t	0
110	18	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-image-1/800/600	Danish Language & Culture Immersion Experience - Image 2	\N	f	f	1
111	18	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-image-2/800/600	Danish Language & Culture Immersion Experience - Image 3	\N	f	f	2
112	18	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-image-3/800/600	Danish Language & Culture Immersion Experience - Image 4	\N	f	f	3
113	18	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-image-4/800/600	Danish Language & Culture Immersion Experience - Image 5	\N	f	f	4
114	18	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-image-5/800/600	Danish Language & Culture Immersion Experience - Image 6	\N	f	f	5
115	19	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-image-0/800/600	Swedish Education System & Teaching Methods Study Tour - Image 1	\N	t	t	0
116	19	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-image-1/800/600	Swedish Education System & Teaching Methods Study Tour - Image 2	\N	f	f	1
117	19	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-image-2/800/600	Swedish Education System & Teaching Methods Study Tour - Image 3	\N	f	f	2
118	19	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-image-3/800/600	Swedish Education System & Teaching Methods Study Tour - Image 4	\N	f	f	3
13	2	https://picsum.photos/seed/shanghai-food-tour-street-food-5/800/600	Shanghai Food Tour: Local Street Food and Hidden Gems - Image 6	\N	f	f	5
14	2	https://picsum.photos/seed/shanghai-food-tour-street-food-6/800/600	Shanghai Food Tour: Local Street Food and Hidden Gems - Image 7	\N	f	f	6
15	3	https://picsum.photos/seed/stockholm-university-study-tour-0/800/600	Stockholm University Campus & Swedish Education System Study Tour - Image 1	\N	t	t	0
16	3	https://picsum.photos/seed/stockholm-university-study-tour-1/800/600	Stockholm University Campus & Swedish Education System Study Tour - Image 2	\N	f	f	1
17	3	https://picsum.photos/seed/stockholm-university-study-tour-2/800/600	Stockholm University Campus & Swedish Education System Study Tour - Image 3	\N	f	f	2
18	3	https://picsum.photos/seed/stockholm-university-study-tour-3/800/600	Stockholm University Campus & Swedish Education System Study Tour - Image 4	\N	f	f	3
19	3	https://picsum.photos/seed/stockholm-university-study-tour-4/800/600	Stockholm University Campus & Swedish Education System Study Tour - Image 5	\N	f	f	4
20	3	https://picsum.photos/seed/stockholm-university-study-tour-5/800/600	Stockholm University Campus & Swedish Education System Study Tour - Image 6	\N	f	f	5
21	3	https://picsum.photos/seed/stockholm-university-study-tour-6/800/600	Stockholm University Campus & Swedish Education System Study Tour - Image 7	\N	f	f	6
22	3	https://picsum.photos/seed/stockholm-university-study-tour-7/800/600	Stockholm University Campus & Swedish Education System Study Tour - Image 8	\N	f	f	7
23	4	https://picsum.photos/seed/copenhagen-design-academy-workshop-0/800/600	Copenhagen Design Academy & Danish Design Philosophy Workshop - Image 1	\N	t	t	0
24	4	https://picsum.photos/seed/copenhagen-design-academy-workshop-1/800/600	Copenhagen Design Academy & Danish Design Philosophy Workshop - Image 2	\N	f	f	1
25	4	https://picsum.photos/seed/copenhagen-design-academy-workshop-2/800/600	Copenhagen Design Academy & Danish Design Philosophy Workshop - Image 3	\N	f	f	2
26	4	https://picsum.photos/seed/copenhagen-design-academy-workshop-3/800/600	Copenhagen Design Academy & Danish Design Philosophy Workshop - Image 4	\N	f	f	3
49	8	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-image-0/800/600	Sichuan Culinary Institute Cooking Masterclass - Image 1	\N	t	t	0
50	8	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-image-1/800/600	Sichuan Culinary Institute Cooking Masterclass - Image 2	\N	f	f	1
51	8	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-image-2/800/600	Sichuan Culinary Institute Cooking Masterclass - Image 3	\N	f	f	2
52	8	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-image-3/800/600	Sichuan Culinary Institute Cooking Masterclass - Image 4	\N	f	f	3
53	8	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-image-4/800/600	Sichuan Culinary Institute Cooking Masterclass - Image 5	\N	f	f	4
54	8	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-image-5/800/600	Sichuan Culinary Institute Cooking Masterclass - Image 6	\N	f	f	5
55	9	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-image-0/800/600	Zhangjiajie Avatar Mountain Photography Adventure - Image 1	\N	t	t	0
56	9	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-image-1/800/600	Zhangjiajie Avatar Mountain Photography Adventure - Image 2	\N	f	f	1
57	9	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-image-2/800/600	Zhangjiajie Avatar Mountain Photography Adventure - Image 3	\N	f	f	2
58	9	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-image-3/800/600	Zhangjiajie Avatar Mountain Photography Adventure - Image 4	\N	f	f	3
59	9	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-image-4/800/600	Zhangjiajie Avatar Mountain Photography Adventure - Image 5	\N	f	f	4
60	9	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-image-5/800/600	Zhangjiajie Avatar Mountain Photography Adventure - Image 6	\N	f	f	5
61	10	https://picsum.photos/seed/beijing-traditional-arts-temple-culture-image-0/800/600	Beijing Traditional Arts & Temple Culture Experience - Image 1	\N	t	t	0
62	10	https://picsum.photos/seed/beijing-traditional-arts-temple-culture-image-1/800/600	Beijing Traditional Arts & Temple Culture Experience - Image 2	\N	f	f	1
63	10	https://picsum.photos/seed/beijing-traditional-arts-temple-culture-image-2/800/600	Beijing Traditional Arts & Temple Culture Experience - Image 3	\N	f	f	2
64	10	https://picsum.photos/seed/beijing-traditional-arts-temple-culture-image-3/800/600	Beijing Traditional Arts & Temple Culture Experience - Image 4	\N	f	f	3
65	10	https://picsum.photos/seed/beijing-traditional-arts-temple-culture-image-4/800/600	Beijing Traditional Arts & Temple Culture Experience - Image 5	\N	f	f	4
66	10	https://picsum.photos/seed/beijing-traditional-arts-temple-culture-image-5/800/600	Beijing Traditional Arts & Temple Culture Experience - Image 6	\N	f	f	5
67	11	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-image-0/800/600	Guangzhou Modern Art & Innovation District Tour - Image 1	\N	t	t	0
68	11	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-image-1/800/600	Guangzhou Modern Art & Innovation District Tour - Image 2	\N	f	f	1
69	11	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-image-2/800/600	Guangzhou Modern Art & Innovation District Tour - Image 3	\N	f	f	2
70	11	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-image-3/800/600	Guangzhou Modern Art & Innovation District Tour - Image 4	\N	f	f	3
71	11	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-image-4/800/600	Guangzhou Modern Art & Innovation District Tour - Image 5	\N	f	f	4
72	11	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-image-5/800/600	Guangzhou Modern Art & Innovation District Tour - Image 6	\N	f	f	5
73	12	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-image-0/800/600	Shanghai Street Food & Night Market Adventure - Image 1	\N	t	t	0
74	12	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-image-1/800/600	Shanghai Street Food & Night Market Adventure - Image 2	\N	f	f	1
75	12	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-image-2/800/600	Shanghai Street Food & Night Market Adventure - Image 3	\N	f	f	2
76	12	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-image-3/800/600	Shanghai Street Food & Night Market Adventure - Image 4	\N	f	f	3
77	12	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-image-4/800/600	Shanghai Street Food & Night Market Adventure - Image 5	\N	f	f	4
119	19	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-image-4/800/600	Swedish Education System & Teaching Methods Study Tour - Image 5	\N	f	f	4
120	19	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-image-5/800/600	Swedish Education System & Teaching Methods Study Tour - Image 6	\N	f	f	5
121	20	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-image-0/800/600	Norwegian Fjords & Arctic Wildlife Photography Expedition - Image 1	\N	t	t	0
122	20	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-image-1/800/600	Norwegian Fjords & Arctic Wildlife Photography Expedition - Image 2	\N	f	f	1
123	20	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-image-2/800/600	Norwegian Fjords & Arctic Wildlife Photography Expedition - Image 3	\N	f	f	2
124	20	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-image-3/800/600	Norwegian Fjords & Arctic Wildlife Photography Expedition - Image 4	\N	f	f	3
125	20	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-image-4/800/600	Norwegian Fjords & Arctic Wildlife Photography Expedition - Image 5	\N	f	f	4
126	20	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-image-5/800/600	Norwegian Fjords & Arctic Wildlife Photography Expedition - Image 6	\N	f	f	5
127	21	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-image-0/800/600	Icelandic Geothermal & Volcanic Landscape Adventure - Image 1	\N	t	t	0
128	21	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-image-1/800/600	Icelandic Geothermal & Volcanic Landscape Adventure - Image 2	\N	f	f	1
129	21	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-image-2/800/600	Icelandic Geothermal & Volcanic Landscape Adventure - Image 3	\N	f	f	2
130	21	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-image-3/800/600	Icelandic Geothermal & Volcanic Landscape Adventure - Image 4	\N	f	f	3
131	21	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-image-4/800/600	Icelandic Geothermal & Volcanic Landscape Adventure - Image 5	\N	f	f	4
132	21	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-image-5/800/600	Icelandic Geothermal & Volcanic Landscape Adventure - Image 6	\N	f	f	5
133	22	https://picsum.photos/seed/stockholm-modern-design-architecture-walking-tour-image-0/800/600	Stockholm Modern Design & Architecture Walking Tour - Image 1	\N	t	t	0
134	22	https://picsum.photos/seed/stockholm-modern-design-architecture-walking-tour-image-1/800/600	Stockholm Modern Design & Architecture Walking Tour - Image 2	\N	f	f	1
135	22	https://picsum.photos/seed/stockholm-modern-design-architecture-walking-tour-image-2/800/600	Stockholm Modern Design & Architecture Walking Tour - Image 3	\N	f	f	2
136	22	https://picsum.photos/seed/stockholm-modern-design-architecture-walking-tour-image-3/800/600	Stockholm Modern Design & Architecture Walking Tour - Image 4	\N	f	f	3
137	22	https://picsum.photos/seed/stockholm-modern-design-architecture-walking-tour-image-4/800/600	Stockholm Modern Design & Architecture Walking Tour - Image 5	\N	f	f	4
138	22	https://picsum.photos/seed/stockholm-modern-design-architecture-walking-tour-image-5/800/600	Stockholm Modern Design & Architecture Walking Tour - Image 6	\N	f	f	5
\.


--
-- TOC entry 4213 (class 0 OID 27293)
-- Dependencies: 259
-- Data for Name: activity_include_translations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activity_include_translations (id, include_id, language, item) FROM stdin;
1	1	zh	专业中文导游服务
2	2	zh	往返酒店交通
3	3	zh	缆车票
4	4	zh	传统中式午餐
5	5	zh	长城门票
6	6	zh	个人消费
7	7	zh	小费
8	1	es	Guía profesional en español
9	2	es	Transporte desde/hacia el hotel
10	3	es	Boletos de teleférico
11	4	es	Almuerzo chino tradicional
12	5	es	Entrada a la Gran Muralla
13	6	es	Gastos personales
14	7	es	Propinas
15	1	fr	Guide professionnel en français
16	2	fr	Transport depuis/vers l'hôtel
17	3	fr	Billets de téléphérique
18	4	fr	Déjeuner chinois traditionnel
19	5	fr	Entrée à la Grande Muraille
20	6	fr	Dépenses personnelles
21	7	fr	Pourboires
22	8	zh	专业美食导游
23	9	zh	所有食物品尝
24	10	zh	市场参观
25	11	zh	烹饪历史讲解
26	12	zh	酒精饮料
27	13	zh	交通费
28	8	es	Guía gastronómico profesional
29	9	es	Todas las degustaciones de comida
30	10	es	Visitas a mercados
31	11	es	Historia culinaria y explicaciones
32	12	es	Bebidas alcohólicas
33	13	es	Gastos de transporte
34	8	fr	Guide gastronomique professionnel
35	9	fr	Toutes les dégustations de nourriture
36	10	fr	Visites de marchés
37	11	fr	Histoire culinaire et explications
38	12	fr	Boissons alcoolisées
39	13	fr	Frais de transport
40	14	zh	校园导览
41	15	zh	学生和教授交流会
42	16	zh	教育体系讲座
43	17	zh	学习资料包
44	18	zh	茶点
45	19	zh	交通费
46	20	zh	个人用餐
47	14	es	Tour del campus
48	15	es	Sesiones con estudiantes y profesores
49	16	es	Conferencias sobre el sistema educativo
50	17	es	Paquete de materiales de estudio
51	18	es	Refrigerios
52	19	es	Gastos de transporte
53	20	es	Comidas personales
54	14	fr	Visite du campus
55	15	fr	Sessions avec étudiants et professeurs
56	16	fr	Conférences sur le système éducatif
57	17	fr	Pack de matériaux d'étude
58	18	fr	Rafraîchissements
59	19	fr	Frais de transport
60	20	fr	Repas personnels
61	35	zh	专业历史导游
62	36	zh	兵马俑博物馆门票
63	37	zh	往返交通
64	38	zh	语音导览设备
65	39	zh	小组照片
66	40	zh	个人消费
67	41	zh	午餐
68	35	es	Guía profesional de historia
69	36	es	Entrada al Museo del Ejército de Terracota
70	37	es	Transporte de ida y vuelta
71	38	es	Equipo de audioguía
72	39	es	Foto grupal
73	40	es	Gastos personales
74	41	es	Almuerzo
75	35	fr	Guide professionnel d'histoire
76	36	fr	Entrée au Musée de l'Armée de Terre Cuite
77	37	fr	Transport aller-retour
78	38	fr	Équipement d'audioguide
79	39	fr	Photo de groupe
80	40	fr	Dépenses personnelles
81	41	fr	Déjeuner
82	42	zh	专业烹饪指导
83	43	zh	所有食材和调料
84	44	zh	烹饪工具使用
85	45	zh	市场参观
86	46	zh	食谱手册
87	47	zh	品尝自制菜肴
88	48	zh	酒精饮料
89	49	zh	交通费
90	42	es	Instrucción culinaria profesional
91	43	es	Todos los ingredientes y especias
92	44	es	Uso de herramientas de cocina
93	45	es	Visita al mercado
94	46	es	Manual de recetas
95	47	es	Degustación de platos preparados
96	48	es	Bebidas alcohólicas
97	49	es	Gastos de transporte
98	42	fr	Instruction culinaire professionnelle
99	43	fr	Tous les ingrédients et épices
100	44	fr	Utilisation d'outils de cuisine
101	45	fr	Visite du marché
102	46	fr	Manuel de recettes
103	47	fr	Dégustation des plats préparés
104	48	fr	Boissons alcoolisées
105	49	fr	Frais de transport
106	50	zh	专业摄影指导
107	51	zh	野生动物观察游船
108	52	zh	摄影设备建议
109	53	zh	小组摄影点评
110	54	zh	热饮和小食
111	55	zh	摄影设备租赁
112	56	zh	住宿
113	50	es	Instrucción fotográfica profesional
114	51	es	Crucero de observación de vida silvestre
115	52	es	Consejos sobre equipo fotográfico
116	53	es	Sesiones de revisión fotográfica grupal
117	54	es	Bebidas calientes y aperitivos
118	55	es	Alquiler de equipo fotográfico
119	56	es	Alojamiento
120	50	fr	Instruction photographique professionnelle
121	51	fr	Croisière d'observation de la faune
122	52	fr	Conseils sur l'équipement photographique
123	53	fr	Sessions de révision photographique de groupe
124	54	fr	Boissons chaudes et collations
125	55	fr	Location d'équipement photographique
126	56	fr	Hébergement
127	78	zh	专业摄影导游
128	79	zh	国家公园门票
129	80	zh	缆车和电梯通行
130	81	zh	摄影技巧指导课程
131	82	zh	小组摄影作品点评
132	83	zh	摄影设备租赁
133	84	zh	餐食和饮料
134	78	es	Guía profesional de fotografía
135	79	es	Entradas al parque nacional
136	80	es	Acceso a teleférico y ascensor
137	81	es	Sesión de consejos y técnicas fotográficas
138	82	es	Revisión grupal de fotos
139	83	es	Alquiler de equipo fotográfico
140	84	es	Comidas y bebidas
141	78	fr	Guide professionnel de photographie
142	79	fr	Billets d'entrée au parc national
143	80	fr	Accès au téléphérique et ascenseur
144	81	fr	Session de conseils et techniques photographiques
145	82	fr	Révision de photos en groupe
146	83	fr	Location d'équipement photographique
147	84	fr	Repas et boissons
148	21	zh	Design Academy guided tour
149	22	zh	2-hour hands-on workshop
150	23	zh	Professional designer meeting
151	24	zh	Design materials and tools
152	25	zh	Traditional Danish lunch
153	26	zh	Personal design consultation
154	27	zh	Workshop materials take-home
155	21	es	Design Academy guided tour
156	22	es	2-hour hands-on workshop
157	23	es	Professional designer meeting
158	24	es	Design materials and tools
159	25	es	Traditional Danish lunch
160	26	es	Personal design consultation
161	27	es	Workshop materials take-home
162	21	fr	Design Academy guided tour
163	22	fr	2-hour hands-on workshop
164	23	fr	Professional designer meeting
165	24	fr	Design materials and tools
166	25	fr	Traditional Danish lunch
167	26	fr	Personal design consultation
168	27	fr	Workshop materials take-home
169	93	zh	Professional art guide
170	94	zh	Gallery and museum entrance fees
171	95	zh	Innovation district walking tour
172	96	zh	Contemporary art discussions
173	97	zh	Artist studio visits
174	98	zh	Refreshments
175	99	zh	Art purchases
176	100	zh	Transportation between venues
177	93	es	Professional art guide
178	94	es	Gallery and museum entrance fees
179	95	es	Innovation district walking tour
180	96	es	Contemporary art discussions
181	97	es	Artist studio visits
182	98	es	Refreshments
183	99	es	Art purchases
184	100	es	Transportation between venues
185	93	fr	Professional art guide
186	94	fr	Gallery and museum entrance fees
187	95	fr	Innovation district walking tour
188	96	fr	Contemporary art discussions
189	97	fr	Artist studio visits
190	98	fr	Refreshments
191	99	fr	Art purchases
192	100	fr	Transportation between venues
193	71	zh	Innovation hub visits
194	72	zh	Startup founder meetings
195	73	zh	Ecosystem overview presentations
196	74	zh	Networking sessions
197	75	zh	Innovation methodology workshops
198	76	zh	Transportation between venues
199	77	zh	Meals and refreshments
200	71	es	Innovation hub visits
201	72	es	Startup founder meetings
202	73	es	Ecosystem overview presentations
203	74	es	Networking sessions
204	75	es	Innovation methodology workshops
205	76	es	Transportation between venues
206	77	es	Meals and refreshments
207	71	fr	Innovation hub visits
208	72	fr	Startup founder meetings
209	73	fr	Ecosystem overview presentations
210	74	fr	Networking sessions
211	75	fr	Innovation methodology workshops
212	76	fr	Transportation between venues
213	77	fr	Meals and refreshments
\.


--
-- TOC entry 4184 (class 0 OID 27017)
-- Dependencies: 230
-- Data for Name: activity_includes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activity_includes (id, activity_id, item, is_included, order_index) FROM stdin;
1	1	Private professional guide	t	0
2	1	Round-trip transportation	t	1
3	1	Cable car tickets	t	2
4	1	Traditional Chinese lunch	t	3
5	1	Entrance fees	t	4
6	1	Personal expenses	f	5
7	1	Gratuities	f	6
8	2	Professional food guide	t	0
9	2	All food tastings (10+ items)	t	1
10	2	Market visits and cultural explanations	t	2
11	2	Small group size (max 8 people)	t	3
12	2	Drinks and additional snacks	f	4
13	2	Transportation to meeting point	f	5
14	3	University campus guided tour	t	0
15	3	Student and professor meetings	t	1
16	3	Educational materials and brochures	t	2
17	3	Traditional Swedish fika (coffee break)	t	3
18	3	Transportation between campus locations	t	4
19	3	University application guidance	f	5
20	3	Personal consultation fees	f	6
21	4	Design Academy guided tour	t	0
22	4	2-hour hands-on workshop	t	1
23	4	Professional designer meeting	t	2
24	4	Design materials and tools	t	3
25	4	Traditional Danish lunch	t	4
26	4	Personal design consultation	f	5
27	4	Workshop materials take-home	f	6
28	5	Expert Northern Lights guide	t	0
29	5	Traditional Sami dinner	t	1
30	5	Arctic clothing and gear	t	2
31	5	Hot beverages and snacks	t	3
32	5	Professional photography guidance	t	4
33	5	Aurora guarantee (return trip if no sighting)	f	5
34	5	Personal camera equipment	f	6
35	6	Expert archaeological guide	t	0
36	6	All excavation pit entries	t	1
37	6	Bronze Chariot Exhibition	t	2
38	6	Round-trip transportation	t	3
39	6	Historical documentation	t	4
40	6	Personal headphones for large groups	f	5
41	6	Lunch and refreshments	f	6
42	8	Professional culinary instruction	t	1
43	8	All ingredients and spices	t	2
44	8	Cooking tools and equipment usage	t	3
45	8	Market visit	t	4
46	8	Recipe booklet	t	5
47	8	Tasting of prepared dishes	t	6
48	8	Alcoholic beverages	f	7
49	8	Transportation costs	f	8
50	20	Professional photography instruction	t	1
51	20	Wildlife viewing cruise	t	2
52	20	Photography equipment guidance	t	3
53	20	Group photo review sessions	t	4
54	20	Hot drinks and snacks	t	5
55	20	Photography equipment rental	f	6
56	20	Accommodation	f	7
57	6	Professional history guide	t	1
58	6	Terracotta Army Museum entrance tickets	t	2
59	6	Round-trip transportation	t	3
60	6	Audio guide equipment	t	4
61	6	Group photo	t	5
62	6	Personal expenses	f	6
63	6	Lunch	f	7
64	16	Campus tour	t	1
65	16	Sessions with students and professors	t	2
66	16	Educational system lectures	t	3
67	16	Study materials package	t	4
68	16	Refreshments	t	5
69	16	Transportation expenses	f	6
70	16	Personal meals	f	7
71	17	Innovation hub visits	t	1
72	17	Startup founder meetings	t	2
73	17	Ecosystem overview presentations	t	3
74	17	Networking sessions	t	4
75	17	Innovation methodology workshops	t	5
76	17	Transportation between venues	f	6
77	17	Meals and refreshments	f	7
78	9	Professional photography guide	t	1
79	9	National park entrance tickets	t	2
80	9	Cable car and elevator access	t	3
81	9	Photography tips and techniques session	t	4
82	9	Group photo review	t	5
83	9	Photography equipment rental	f	6
84	9	Meals and beverages	f	7
85	10	Expert cultural guide	t	1
86	10	Temple entrance fees	t	2
87	10	Traditional art demonstrations	t	3
88	10	Hands-on cultural activities	t	4
89	10	Tea ceremony experience	t	5
90	10	Cultural workshop materials	t	6
91	10	Personal purchases	f	7
92	10	Transportation costs	f	8
93	11	Professional art guide	t	1
94	11	Gallery and museum entrance fees	t	2
95	11	Innovation district walking tour	t	3
96	11	Contemporary art discussions	t	4
97	11	Artist studio visits	t	5
98	11	Refreshments	t	6
99	11	Art purchases	f	7
100	11	Transportation between venues	f	8
101	12	Local food expert guide	t	1
102	12	All food tastings and samples	t	2
103	12	Night market exploration	t	3
104	12	Street food history and culture	t	4
105	12	Food safety guidance	t	5
106	12	Alcoholic beverages	f	6
107	12	Additional food purchases	f	7
108	13	Bamboo raft experience	t	1
109	13	Professional raft guide	t	2
110	13	Scenic Li River journey	t	3
111	13	Countryside village visit	t	4
112	13	Traditional fishing demonstration	t	5
113	13	Life jackets and safety equipment	t	6
114	13	Meals and snacks	f	7
115	13	Transportation to rafting point	f	8
116	14	Expert cultural guide	t	1
117	14	West Lake scenic walk	t	2
118	14	Historical site visits	t	3
119	14	Traditional tea house experience	t	4
120	14	Cultural stories and legends	t	5
121	14	Group photos at scenic spots	t	6
122	14	Tea and refreshments	f	7
123	14	Souvenir purchases	f	8
124	15	Professional history guide	t	1
125	15	Muslim Quarter walking tour	t	2
126	15	Silk Road museum visit	t	3
127	15	Traditional handicraft demonstrations	t	4
128	15	Local food tastings	t	5
129	15	Historical storytelling	t	6
130	15	Souvenir shopping	f	7
131	15	Additional meals	f	8
132	18	Danish language instruction	t	1
133	18	Cultural activities and games	t	2
134	18	Local interaction opportunities	t	3
135	18	Danish cultural insights	t	4
136	18	Language learning materials	t	5
137	18	Traditional Danish refreshments	t	6
138	18	Transportation costs	f	7
139	18	Personal expenses	f	8
140	19	Educational expert guide	t	1
141	19	School visits and observations	t	2
142	19	Teacher and student interactions	t	3
143	19	Educational methodology presentations	t	4
144	19	Research materials and reports	t	5
145	19	Networking opportunities	t	6
146	19	Transportation between schools	f	7
147	19	Meals and accommodation	f	8
148	21	Geological expert guide	t	1
149	21	Geothermal site visits	t	2
150	21	Volcanic landscape exploration	t	3
151	21	Hot spring experience	t	4
152	21	Geological education	t	5
153	21	Safety equipment	t	6
154	21	Meals and beverages	f	7
155	21	Transportation costs	f	8
156	22	Professional architecture guide	t	1
157	22	Modern design district tour	t	2
158	22	Architectural landmark visits	t	3
159	22	Design philosophy discussions	t	4
160	22	Interior design showcases	t	5
161	22	Design museum insights	t	6
162	22	Museum entrance fees	f	7
163	22	Design purchases	f	8
\.


--
-- TOC entry 4219 (class 0 OID 27344)
-- Dependencies: 265
-- Data for Name: activity_pricing_tier_translations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activity_pricing_tier_translations (id, pricing_tier_id, language, tier_name, tier_description) FROM stdin;
\.


--
-- TOC entry 4194 (class 0 OID 27092)
-- Dependencies: 240
-- Data for Name: activity_pricing_tiers; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activity_pricing_tiers (id, activity_id, tier_name, tier_description, price_adult, price_child, order_index, is_active) FROM stdin;
1	1	Standard	Basic tour experience with professional guide	89.00	62.30	0	t
2	1	Premium	Enhanced experience with additional perks and smaller groups	115.70	80.99	1	t
3	1	VIP	Luxury experience with private guide and exclusive access	160.20	112.14	2	t
4	2	Standard	Basic tour experience with professional guide	65.00	45.50	0	t
5	2	Premium	Enhanced experience with additional perks and smaller groups	84.50	59.15	1	t
6	2	VIP	Luxury experience with private guide and exclusive access	117.00	81.90	2	t
7	3	Standard	Basic tour experience with professional guide	120.00	84.00	0	t
8	3	Premium	Enhanced experience with additional perks and smaller groups	156.00	109.20	1	t
9	3	VIP	Luxury experience with private guide and exclusive access	216.00	151.20	2	t
10	4	Standard	Basic tour experience with professional guide	95.00	66.50	0	t
11	4	Premium	Enhanced experience with additional perks and smaller groups	123.50	86.45	1	t
12	4	VIP	Luxury experience with private guide and exclusive access	171.00	119.70	2	t
13	5	Standard	Basic tour experience with professional guide	145.00	101.50	0	t
14	5	Premium	Enhanced experience with additional perks and smaller groups	188.50	131.95	1	t
15	5	VIP	Luxury experience with private guide and exclusive access	261.00	182.70	2	t
16	6	Standard	Basic tour experience with professional guide	75.00	52.50	0	t
17	6	Premium	Enhanced experience with additional perks and smaller groups	97.50	68.25	1	t
18	6	VIP	Luxury experience with private guide and exclusive access	135.00	94.50	2	t
22	8	Standard	Basic experience with all core activities	120.00	84.00	0	t
23	8	Premium	Enhanced experience with additional perks	168.00	117.60	1	t
24	8	VIP	Luxury experience with exclusive access	216.00	151.20	2	t
25	9	Standard	Basic experience with all core activities	180.00	126.00	0	t
26	9	Premium	Enhanced experience with additional perks	252.00	176.40	1	t
27	9	VIP	Luxury experience with exclusive access	324.00	226.80	2	t
28	10	Standard	Basic experience with all core activities	85.00	59.50	0	t
29	10	Premium	Enhanced experience with additional perks	119.00	83.30	1	t
30	10	VIP	Luxury experience with exclusive access	153.00	107.10	2	t
31	11	Standard	Basic experience with all core activities	75.00	52.50	0	t
32	11	Premium	Enhanced experience with additional perks	105.00	73.50	1	t
33	11	VIP	Luxury experience with exclusive access	135.00	94.50	2	t
34	12	Standard	Basic experience with all core activities	65.00	45.50	0	t
35	12	Premium	Enhanced experience with additional perks	91.00	63.70	1	t
36	12	VIP	Luxury experience with exclusive access	117.00	81.90	2	t
37	13	Standard	Basic experience with all core activities	95.00	66.50	0	t
38	13	Premium	Enhanced experience with additional perks	133.00	93.10	1	t
39	13	VIP	Luxury experience with exclusive access	171.00	119.70	2	t
40	14	Standard	Basic experience with all core activities	70.00	49.00	0	t
41	14	Premium	Enhanced experience with additional perks	98.00	68.60	1	t
42	14	VIP	Luxury experience with exclusive access	126.00	88.20	2	t
43	15	Standard	Basic experience with all core activities	80.00	56.00	0	t
44	15	Premium	Enhanced experience with additional perks	112.00	78.40	1	t
45	15	VIP	Luxury experience with exclusive access	144.00	100.80	2	t
46	16	Standard	Basic experience with all core activities	150.00	105.00	0	t
47	16	Premium	Enhanced experience with additional perks	210.00	147.00	1	t
48	16	VIP	Luxury experience with exclusive access	270.00	189.00	2	t
49	17	Standard	Basic experience with all core activities	140.00	98.00	0	t
50	17	Premium	Enhanced experience with additional perks	196.00	137.20	1	t
51	17	VIP	Luxury experience with exclusive access	252.00	176.40	2	t
52	18	Standard	Basic experience with all core activities	110.00	77.00	0	t
53	18	Premium	Enhanced experience with additional perks	154.00	107.80	1	t
54	18	VIP	Luxury experience with exclusive access	198.00	138.60	2	t
55	19	Standard	Basic experience with all core activities	135.00	94.50	0	t
56	19	Premium	Enhanced experience with additional perks	189.00	132.30	1	t
57	19	VIP	Luxury experience with exclusive access	243.00	170.10	2	t
58	20	Standard	Basic experience with all core activities	220.00	154.00	0	t
59	20	Premium	Enhanced experience with additional perks	308.00	215.60	1	t
60	20	VIP	Luxury experience with exclusive access	396.00	277.20	2	t
61	21	Standard	Basic experience with all core activities	195.00	136.50	0	t
62	21	Premium	Enhanced experience with additional perks	273.00	191.10	1	t
63	21	VIP	Luxury experience with exclusive access	351.00	245.70	2	t
64	22	Standard	Basic experience with all core activities	75.00	52.50	0	t
65	22	Premium	Enhanced experience with additional perks	105.00	73.50	1	t
66	22	VIP	Luxury experience with exclusive access	135.00	94.50	2	t
\.


--
-- TOC entry 4192 (class 0 OID 27079)
-- Dependencies: 238
-- Data for Name: activity_time_slots; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activity_time_slots (id, activity_id, slot_time, slot_label, max_capacity, is_available, price_adjustment) FROM stdin;
1	1	09:00	Morning	150	t	0.00
2	1	14:00	Afternoon	100	t	0.00
3	1	18:00	Evening	50	t	0.00
4	2	09:00	Morning	150	t	0.00
5	2	14:00	Afternoon	100	t	0.00
6	2	18:00	Evening	50	t	0.00
7	3	09:00	Morning	150	t	0.00
8	3	14:00	Afternoon	100	t	0.00
9	3	18:00	Evening	50	t	0.00
10	4	09:00	Morning	150	t	0.00
11	4	14:00	Afternoon	100	t	0.00
12	4	18:00	Evening	50	t	0.00
13	5	09:00	Morning	150	t	0.00
14	5	14:00	Afternoon	100	t	0.00
15	5	18:00	Evening	50	t	0.00
16	6	09:00	Morning	150	t	0.00
17	6	14:00	Afternoon	100	t	0.00
18	6	18:00	Evening	50	t	0.00
\.


--
-- TOC entry 4217 (class 0 OID 27327)
-- Dependencies: 263
-- Data for Name: activity_timeline_translations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activity_timeline_translations (id, timeline_id, language, title, description) FROM stdin;
1	36	zh	相见欢迎	与您的大师厨师和其他学员见面，简单介绍今天的烹饪课程和四川菜的历史。
2	37	zh	市场探索	参观当地香料市场，了解正宗川菜食材，学习如何选择最好的花椒和辣椒。
3	38	zh	烹饪技巧	学习经典川菜的核心烹饪技巧，包括如何平衡'麻辣'口味和刀工技术。
4	39	zh	制作经典菜肴	亲手制作麻婆豆腐、宫保鸡丁和担担面，掌握每道菜的独特调味秘诀。
5	40	zh	品尝分享	享用您亲手制作的美味川菜，与其他学员分享烹饪心得，获得正宗食谱。
6	36	es	Encuentro y Bienvenida	Conoce a tu chef maestro y otros participantes, breve introducción al programa de cocina y la historia de la cocina de Sichuan.
7	37	es	Exploración del Mercado	Visita el mercado local de especias, aprende sobre ingredientes auténticos de Sichuan y cómo seleccionar los mejores pimientos Sichuan y chiles.
8	38	es	Técnicas Culinarias	Aprende las técnicas de cocina fundamentales de los platos clásicos de Sichuan, incluyendo cómo equilibrar los sabores 'mala' y técnicas de cuchillo.
9	39	es	Preparación de Platos Clásicos	Prepara con tus propias manos Mapo Tofu, Pollo Kung Pao y Fideos Dan Dan, dominando los secretos únicos de condimentado de cada plato.
10	40	es	Degustación y Compartir	Disfruta de la deliciosa cocina de Sichuan que preparaste, comparte experiencias culinarias con otros participantes y recibe recetas auténticas.
11	36	fr	Rencontre et Accueil	Rencontrez votre chef maître et les autres participants, brève introduction au programme de cuisine et à l'histoire de la cuisine du Sichuan.
12	37	fr	Exploration du Marché	Visitez le marché local d'épices, apprenez les ingrédients authentiques du Sichuan et comment sélectionner les meilleurs poivres du Sichuan et piments.
13	38	fr	Techniques Culinaires	Apprenez les techniques de cuisine fondamentales des plats classiques du Sichuan, y compris comment équilibrer les saveurs 'mala' et les techniques de couteau.
14	39	fr	Préparation de Plats Classiques	Préparez de vos propres mains le Mapo Tofu, le Poulet Kung Pao et les Nouilles Dan Dan, maîtrisant les secrets uniques d'assaisonnement de chaque plat.
15	40	fr	Dégustation et Partage	Dégustez la délicieuse cuisine du Sichuan que vous avez préparée, partagez des expériences culinaires avec d'autres participants et recevez des recettes authentiques.
16	1	zh	酒店接送	早上从您的酒店出发，舒适的私人车辆前往慕田峪长城，途中导游介绍长城历史。
17	2	zh	到达长城	抵达慕田峪长城景区，乘坐缆车或选择徒步登上长城，开始您的历史探索之旅。
18	3	zh	长城徒步	在壮丽的长城上徒步2-3小时，拍摄美丽照片，聆听关于明朝建筑技术的专业讲解。
19	4	zh	传统午餐	在当地餐厅享用正宗中式午餐，品尝北京特色菜肴，补充体力继续下午行程。
20	5	zh	返回酒店	下午返回北京市区，途中可选择参观长城纪念品商店，安全送达您的酒店。
21	1	es	Recogida en Hotel	Salida matutina desde tu hotel en vehículo privado cómodo hacia la Gran Muralla de Mutianyu, con introducción histórica durante el viaje.
22	2	es	Llegada a la Gran Muralla	Llegada al área de la Gran Muralla de Mutianyu, toma el teleférico o elige caminar hasta la muralla para comenzar tu exploración histórica.
23	3	es	Caminata por la Gran Muralla	Camina por la magnífica Gran Muralla durante 2-3 horas, toma hermosas fotos y escucha explicaciones expertas sobre las técnicas de construcción Ming.
24	4	es	Almuerzo Tradicional	Disfruta de un auténtico almuerzo chino en un restaurante local, prueba platos especiales de Beijing y repón energías para la tarde.
25	5	es	Regreso al Hotel	Regreso a la ciudad de Beijing por la tarde, con opción de visitar tienda de souvenirs de la Gran Muralla, entrega segura en tu hotel.
26	1	fr	Prise en Charge à l'Hôtel	Départ matinal depuis votre hôtel en véhicule privé confortable vers la Grande Muraille de Mutianyu, avec introduction historique pendant le voyage.
27	2	fr	Arrivée à la Grande Muraille	Arrivée à la zone de la Grande Muraille de Mutianyu, prenez le téléphérique ou choisissez de marcher jusqu'à la muraille pour commencer votre exploration historique.
28	3	fr	Randonnée sur la Grande Muraille	Marchez sur la magnifique Grande Muraille pendant 2-3 heures, prenez de belles photos et écoutez des explications expertes sur les techniques de construction Ming.
29	4	fr	Déjeuner Traditionnel	Dégustez un déjeuner chinois authentique dans un restaurant local, goûtez des plats spéciaux de Beijing et rechargez vos batteries pour l'après-midi.
30	5	fr	Retour à l'Hôtel	Retour à la ville de Beijing dans l'après-midi, avec option de visiter la boutique de souvenirs de la Grande Muraille, livraison sûre à votre hôtel.
31	26	zh	集合出发	早上在指定地点集合，乘坐舒适巴士前往兵马俑博物馆，导游介绍秦朝历史背景。
32	27	zh	博物馆参观	参观兵马俑博物馆三个坑，观看数千个独特的陶制战士，了解考古发现过程。
33	28	zh	历史讲解	专业导游详细讲解秦始皇的传奇故事、中国统一历史和古代军事文化。
34	29	zh	文物观赏	参观出土文物展厅，近距离观察青铜车马、兵器等珍贵历史文物。
35	30	zh	结束返程	参观结束后拍照留念，返回西安市区，结束这次难忘的历史文化之旅。
36	26	es	Reunión y Salida	Reunión matutina en el punto designado, viaje en autobús cómodo al Museo del Ejército de Terracota con introducción histórica de la Dinastía Qin.
37	27	es	Visita al Museo	Visita las tres fosas del Museo del Ejército de Terracota, observa miles de guerreros de terracota únicos y aprende sobre el proceso de descubrimiento arqueológico.
38	28	es	Explicación Histórica	El guía profesional explica detalladamente la historia legendaria del Emperador Qin Shi Huang, la historia de unificación china y la cultura militar antigua.
39	29	es	Apreciación de Artefactos	Visita la sala de exhibición de artefactos excavados, observa de cerca carros y caballos de bronce, armas y otros artefactos históricos preciosos.
40	30	es	Finalización y Regreso	Después de la visita, toma fotos conmemorativas y regresa al centro de Xi'an, terminando este inolvidable viaje de historia y cultura.
41	26	fr	Rassemblement et Départ	Rassemblement matinal au point désigné, voyage en bus confortable vers le Musée de l'Armée de Terre Cuite avec introduction historique de la Dynastie Qin.
42	27	fr	Visite du Musée	Visitez les trois fosses du Musée de l'Armée de Terre Cuite, observez des milliers de guerriers en terre cuite uniques et apprenez le processus de découverte archéologique.
43	28	fr	Explication Historique	Le guide professionnel explique en détail l'histoire légendaire de l'Empereur Qin Shi Huang, l'histoire de l'unification chinoise et la culture militaire ancienne.
44	29	fr	Appréciation d'Artefacts	Visitez la salle d'exposition d'artefacts excavés, observez de près les chars et chevaux en bronze, les armes et autres artefacts historiques précieux.
45	30	fr	Fin et Retour	Après la visite, prenez des photos commémoratives et retournez au centre de Xi'an, terminant ce voyage inoubliable d'histoire et de culture.
46	96	zh	集合准备	早上在港口集合，检查摄影设备，专业摄影师介绍今日拍摄计划和极地摄影技巧。
47	97	zh	峡湾巡航	乘船进入壮丽的挪威峡湾，开始拍摄雄伟的山脉、瀑布和冰川景观。
48	98	zh	野生动物观察	寻找和拍摄海豹、鲸鱼、海鸟等北极野生动物，学习野生动物摄影技巧。
49	99	zh	摄影指导	专业摄影师提供一对一指导，教授极地光线运用和构图技巧，提升摄影水平。
50	100	zh	作品分享	返回港口后举行摄影作品分享会，互相欣赏今日拍摄成果，获得专业点评。
51	96	es	Reunión y Preparación	Reunión matutina en el puerto, verificación de equipo fotográfico, el fotógrafo profesional introduce el plan de toma del día y técnicas de fotografía polar.
52	97	es	Crucero por Fiordos	Navega hacia los magníficos fiordos noruegos, comienza a fotografiar majestuosas montañas, cascadas y paisajes glaciares.
53	98	es	Observación de Vida Silvestre	Busca y fotografía focas, ballenas, aves marinas y otra vida silvestre ártica, aprende técnicas de fotografía de vida silvestre.
54	99	es	Orientación Fotográfica	El fotógrafo profesional proporciona orientación individual, enseña el uso de luz polar y técnicas de composición para mejorar habilidades fotográficas.
55	100	es	Compartir Obras	Después de regresar al puerto, sesión para compartir trabajos fotográficos, apreciar mutuamente los resultados del día y recibir críticas profesionales.
56	96	fr	Rassemblement et Préparation	Rassemblement matinal au port, vérification de l'équipement photographique, le photographe professionnel présente le plan de prise de vue du jour et les techniques de photographie polaire.
57	97	fr	Croisière dans les Fjords	Naviguez vers les magnifiques fjords norvégiens, commencez à photographier les majestueuses montagnes, cascades et paysages glaciaires.
58	98	fr	Observation de la Faune	Recherchez et photographiez phoques, baleines, oiseaux marins et autre faune arctique, apprenez les techniques de photographie de la faune.
59	99	fr	Orientation Photographique	Le photographe professionnel fournit une orientation individuelle, enseigne l'utilisation de la lumière polaire et les techniques de composition pour améliorer les compétences photographiques.
60	100	fr	Partage d'Œuvres	Après le retour au port, session de partage de travaux photographiques, appréciation mutuelle des résultats du jour et réception de critiques professionnelles.
61	6	zh	集合介绍	在指定地点与美食导游和其他参与者见面，介绍今日美食探索路线和上海街头小食文化。
62	7	zh	传统市场探索	参观热闹的湿货市场，了解新鲜食材，观察当地人的购物习惯和食材选择。
63	8	zh	街头小食品尝	品尝经典上海小食如小笼包、生煎包、煎饼果子等，学习每种食物的历史和制作工艺。
64	9	zh	隐藏宝藏发现	探访只有当地人知道的隐秘美食店，品尝地道家常菜和特色小食。
65	10	zh	美食文化分享	在最后一站总结今日美食体验，分享对上海饮食文化的新认识和感受。
66	6	es	Encuentro e Introducción	Conoce a tu guía gastronómico y otros participantes en el punto designado, introducción a la ruta de exploración gastronómica y cultura de comida callejera de Shanghai.
67	7	es	Exploración de Mercado Tradicional	Visita un mercado húmedo bullicioso, aprende sobre ingredientes frescos, observa hábitos de compra locales y selección de ingredientes.
68	8	es	Degustación de Comida Callejera	Prueba clásicos de Shanghai como xiaolongbao, shengjianbao, jianbing, etc., aprende la historia y proceso de elaboración de cada comida.
69	9	es	Descubrimiento de Joyas Ocultas	Explora restaurantes secretos conocidos solo por locales, prueba cocina casera auténtica y especialidades locales.
70	10	es	Compartir Cultura Gastronómica	En la última parada, resume la experiencia gastronómica del día, comparte nuevos conocimientos y sentimientos sobre la cultura culinaria de Shanghai.
71	6	fr	Rencontre et Introduction	Rencontrez votre guide gastronomique et autres participants au point désigné, introduction à la route d'exploration gastronomique et culture de street food de Shanghai.
72	7	fr	Exploration du Marché Traditionnel	Visitez un marché animé, apprenez sur les ingrédients frais, observez les habitudes d'achat locales et la sélection d'ingrédients.
73	8	fr	Dégustation de Street Food	Goûtez les classiques de Shanghai comme xiaolongbao, shengjianbao, jianbing, etc., apprenez l'histoire et le processus de fabrication de chaque aliment.
74	9	fr	Découverte de Trésors Cachés	Explorez des restaurants secrets connus seulement des locaux, goûtez la cuisine maison authentique et les spécialités locales.
75	10	fr	Partage de Culture Gastronomique	Au dernier arrêt, résumez l'expérience gastronomique du jour, partagez nouvelles connaissances et sentiments sur la culture culinaire de Shanghai.
76	11	zh	校园迎接	在斯德哥尔摩大学主入口与教育专家导游会面，简单介绍今日学习行程和瑞典教育体系概况。
77	12	zh	校园参观	参观现代化校园设施，包括图书馆、实验室、学生活动中心，了解瑞典大学的学习环境。
78	13	zh	教授交流	与瑞典教授进行座谈，深入了解瑞典高等教育的教学理念和研究方法。
79	14	zh	学生互动	与国际学生交流，了解他们在瑞典的学习体验和生活感受。
80	15	zh	教育总结	总结今日所学，获得瑞典教育体系的深入认识和学习资源。
81	11	es	Bienvenida en el Campus	Conoce al guía experto en educación en la entrada principal de la Universidad de Estocolmo, breve introducción al itinerario de aprendizaje y sistema educativo sueco.
82	12	es	Tour del Campus	Visita las instalaciones modernas del campus, incluyendo biblioteca, laboratorios, centro de actividades estudiantiles, comprende el ambiente de aprendizaje de las universidades suecas.
83	13	es	Intercambio con Profesores	Charla con profesores suecos, comprende profundamente la filosofía de enseñanza e investigación de la educación superior sueca.
84	14	es	Interacción con Estudiantes	Intercambia con estudiantes internacionales, aprende sobre su experiencia de aprendizaje y sentimientos de vida en Suecia.
85	15	es	Resumen Educativo	Resume lo aprendido hoy, obtén un entendimiento profundo y recursos de aprendizaje del sistema educativo sueco.
86	11	fr	Accueil sur le Campus	Rencontrez le guide expert en éducation à l'entrée principale de l'Université de Stockholm, brève introduction à l'itinéraire d'apprentissage et au système éducatif suédois.
87	12	fr	Visite du Campus	Visitez les installations modernes du campus, y compris bibliothèque, laboratoires, centre d'activités étudiantes, comprenez l'environnement d'apprentissage des universités suédoises.
88	13	fr	Échange avec les Professeurs	Discussion avec des professeurs suédois, comprenez profondément la philosophie d'enseignement et de recherche de l'enseignement supérieur suédois.
89	14	fr	Interaction avec les Étudiants	Échangez avec des étudiants internationaux, apprenez leur expérience d'apprentissage et sentiments de vie en Suède.
90	15	fr	Résumé Éducatif	Résumez ce qui a été appris aujourd'hui, obtenez une compréhension profonde et des ressources d'apprentissage du système éducatif suédois.
91	21	zh	北极圈欢迎	抵达北极圈城市，与北极文化专家导游见面，介绍北极光科学知识和今日活动安排。
92	22	zh	萨米文化体验	参访萨米族社区，了解这个古老民族的传统生活方式、手工艺制作和驯鹿放牧文化。
93	23	zh	北极生存技能	学习基本的北极生存技巧，包括在极地环境中保暖、导航和安全知识。
94	24	zh	北极光追踪	在最佳观测点等待北极光出现，学习摄影技巧记录这一神奇的自然现象。
95	25	zh	北极夜宿	在传统北极住宿中过夜，品尝当地美食，分享今日的北极体验和文化感受。
96	21	es	Bienvenida al Círculo Ártico	Llegada a la ciudad del Círculo Ártico, encuentro con guía experto en cultura ártica, introducción a la ciencia de auroras boreales y actividades del día.
97	22	es	Experiencia Cultural Sami	Visita a la comunidad Sami, aprende sobre el estilo de vida tradicional de esta antigua nación, artesanías y cultura de pastoreo de renos.
98	23	es	Habilidades de Supervivencia Ártica	Aprende técnicas básicas de supervivencia ártica, incluyendo mantenerse caliente, navegación y conocimiento de seguridad en ambientes polares.
99	24	es	Persecución de Auroras Boreales	Espera la aparición de auroras boreales en el mejor punto de observación, aprende técnicas fotográficas para registrar este fenómeno natural mágico.
100	25	es	Noche Ártica	Pasa la noche en alojamiento ártico tradicional, degusta cocina local, comparte experiencias árticas del día y sentimientos culturales.
101	21	fr	Accueil au Cercle Arctique	Arrivée à la ville du Cercle Arctique, rencontre avec guide expert en culture arctique, introduction à la science des aurores boréales et activités du jour.
102	22	fr	Expérience Culturelle Sami	Visite de la communauté Sami, apprenez le mode de vie traditionnel de cette ancienne nation, l'artisanat et la culture d'élevage de rennes.
103	23	fr	Compétences de Survie Arctique	Apprenez les techniques de base de survie arctique, y compris rester au chaud, navigation et connaissances de sécurité dans les environnements polaires.
104	24	fr	Chasse aux Aurores Boréales	Attendez l'apparition des aurores boréales au meilleur point d'observation, apprenez les techniques photographiques pour enregistrer ce phénomène naturel magique.
105	25	fr	Nuit Arctique	Passez la nuit dans un hébergement arctique traditionnel, dégustez la cuisine locale, partagez les expériences arctiques du jour et sentiments culturels.
106	41	zh	张家界欢迎	抵达张家界市，与专业摄影导游会面，介绍今日拍摄计划和阿凡达取景地背景故事。
107	42	zh	百龙天梯体验	乘坐世界最高的户外电梯上升至袁家界，开始拍摄垂直石柱群的壮观景象。
108	43	zh	阿凡达取景地	在'哈利路亚山'等标志性地点拍摄，学习如何捕捉薄雾中的神秘峰林景观。
109	44	zh	玻璃栈道探险	挑战天门山玻璃栈道，从独特角度拍摄峡谷和山峰的震撼画面。
110	45	zh	日落摄影	在最佳观景台等待日落时分，拍摄金色阳光照耀下的峰林剪影。
111	41	es	Bienvenida a Zhangjiajie	Llegada a la ciudad de Zhangjiajie, encuentro con guía fotográfico profesional, introducción al plan de fotografía del día y historia de fondo de las locaciones de Avatar.
112	42	es	Experiencia del Ascensor Bailong	Toma el ascensor exterior más alto del mundo para subir a Yuanjiajie, comienza a fotografiar la vista espectacular de grupos de pilares verticales.
113	43	es	Locaciones de Avatar	Fotografía en lugares icónicos como las 'Montañas Aleluya', aprende cómo capturar paisajes misteriosos de bosques de picos en la neblina.
114	44	es	Aventura del Sendero de Cristal	Desafía el sendero de cristal de Tianmen, fotografía vistas impactantes de cañones y montañas desde ángulos únicos.
115	45	es	Fotografía del Atardecer	Espera el atardecer en la mejor plataforma de observación, fotografía siluetas de bosques de picos bajo la luz dorada del sol.
116	41	fr	Accueil à Zhangjiajie	Arrivée à la ville de Zhangjiajie, rencontre avec guide photographique professionnel, introduction au plan de photographie du jour et histoire de fond des lieux de tournage d'Avatar.
117	42	fr	Expérience de l'Ascenseur Bailong	Prenez l'ascenseur extérieur le plus haut du monde pour monter à Yuanjiajie, commencez à photographier la vue spectaculaire de groupes de piliers verticaux.
118	43	fr	Lieux de Tournage d'Avatar	Photographiez dans des lieux iconiques comme les 'Montagnes Alléluia', apprenez comment capturer des paysages mystérieux de forêts de pics dans la brume.
119	44	fr	Aventure du Sentier de Verre	Défiez le sentier de verre de Tianmen, photographiez des vues saisissantes de canyons et montagnes sous des angles uniques.
120	45	fr	Photographie du Coucher de Soleil	Attendez le coucher de soleil à la meilleure plateforme d'observation, photographiez des silhouettes de forêts de pics sous la lumière dorée du soleil.
121	46	zh	古都文化迎接	在北京市中心与文化专家导游会面，介绍今日的传统艺术和寺庙文化探索之旅。
122	47	zh	古寺参访	参观天坛和雍和宫，了解中国古代建筑艺术和宗教文化的深厚内涵。
123	48	zh	传统艺术学习	在专业工作室学习书法、国画等传统艺术，体验中国文化的精髓。
124	49	zh	手工艺体验	尝试剪纸、篆刻等传统手工艺制作，感受匠人精神和艺术创造的乐趣。
125	50	zh	茶艺文化	参加传统茶艺仪式，在品茶中感受中国文化的宁静与深邃。
126	46	es	Bienvenida Cultural de la Capital Antigua	Encuentro con guía experto cultural en el centro de Beijing, introducción al viaje de exploración de artes tradicionales y cultura de templos del día.
127	47	es	Visita a Templos Antiguos	Visita el Templo del Cielo y Templo Lama, comprende las profundas connotaciones del arte arquitectónico chino antiguo y cultura religiosa.
128	48	es	Aprendizaje de Artes Tradicionales	Aprende artes tradicionales como caligrafía y pintura china en estudio profesional, experimenta la esencia de la cultura china.
129	49	es	Experiencia de Artesanías	Intenta hacer artesanías tradicionales como papel cortado y grabado de sellos, siente el espíritu artesanal y la alegría de la creación artística.
130	50	es	Cultura del Té	Participa en ceremonia de té tradicional, siente la tranquilidad y profundidad de la cultura china mientras bebes té.
131	46	fr	Accueil Culturel de l'Ancienne Capitale	Rencontre avec guide expert culturel au centre de Beijing, introduction au voyage d'exploration des arts traditionnels et culture des temples du jour.
132	47	fr	Visite de Temples Anciens	Visitez le Temple du Ciel et Temple Lama, comprenez les connotations profondes de l'art architectural chinois ancien et culture religieuse.
133	48	fr	Apprentissage des Arts Traditionnels	Apprenez les arts traditionnels comme calligraphie et peinture chinoise dans studio professionnel, vivez l'essence de la culture chinoise.
134	49	fr	Expérience d'Artisanat	Essayez de faire des artisanats traditionnels comme découpage de papier et gravure de sceaux, ressentez l'esprit artisanal et la joie de création artistique.
135	50	fr	Culture du Thé	Participez à la cérémonie de thé traditionnelle, ressentez la tranquillité et profondeur de la culture chinoise en buvant du thé.
136	16	zh	设计学院欢迎	抵达哥本哈根设计学院，与设计教授和学生见面，介绍丹麦设计历史和今日学习计划。
137	17	zh	设计哲学讲座	参加关于丹麦设计哲学的专业讲座，了解简约主义、功能性和人性化设计的核心理念。
138	18	zh	工作室参观	参观各个设计工作室，观察设计师的创作过程，了解从概念到成品的设计流程。
139	19	zh	实践工作坊	参与实际设计项目，运用丹麦设计原则创作自己的作品，获得专业指导。
140	20	zh	设计文化交流	与设计师和学生深入交流，分享设计理念，了解丹麦设计在全球的影响力。
141	16	es	Bienvenida a la Academia de Diseño	Llegada a la Academia de Diseño de Copenhague, encuentro con profesores de diseño y estudiantes, introducción a la historia del diseño danés y plan de aprendizaje del día.
142	17	es	Conferencia de Filosofía del Diseño	Asiste a conferencia profesional sobre filosofía del diseño danés, comprende conceptos centrales de minimalismo, funcionalidad y diseño humanizado.
143	18	es	Visita a Estudios	Visita varios estudios de diseño, observa el proceso creativo de diseñadores, comprende el flujo de diseño desde concepto hasta producto terminado.
144	19	es	Taller Práctico	Participa en proyecto de diseño actual, aplica principios del diseño danés para crear tu propia obra, recibe orientación profesional.
145	20	es	Intercambio Cultural de Diseño	Intercambia profundamente con diseñadores y estudiantes, comparte conceptos de diseño, comprende la influencia global del diseño danés.
146	16	fr	Accueil à l'Académie de Design	Arrivée à l'Académie de Design de Copenhague, rencontre avec professeurs de design et étudiants, introduction à l'histoire du design danois et plan d'apprentissage du jour.
147	17	fr	Conférence de Philosophie du Design	Assistez à une conférence professionnelle sur la philosophie du design danois, comprenez les concepts centraux du minimalisme, fonctionnalité et design humanisé.
148	18	fr	Visite des Studios	Visitez divers studios de design, observez le processus créatif des designers, comprenez le flux de design du concept au produit fini.
149	19	fr	Atelier Pratique	Participez à un projet de design actuel, appliquez les principes du design danois pour créer votre propre œuvre, recevez des conseils professionnels.
150	20	fr	Échange Culturel de Design	Échangez profondément avec designers et étudiants, partagez concepts de design, comprenez l'influence globale du design danois.
151	51	zh	艺术区集合	在广州现代艺术区集合，与专业艺术导游见面，介绍今日的艺术探索路线。
152	52	zh	画廊巡礼	参观多个知名现代艺术画廊，欣赏当代中国艺术作品，了解艺术发展趋势。
153	53	zh	创意园区探索	游览红砖厂等著名创意园区，感受传统工业建筑与现代艺术的碰撞。
154	54	zh	艺术家工作室	参访活跃艺术家的工作室，观察创作过程，与艺术家面对面交流。
155	55	zh	文化交流总结	在艺术咖啡厅总结今日体验，分享对广州现代艺术和创新文化的感受。
156	51	es	Reunión en Distrito Artístico	Reunión en el distrito de arte moderno de Guangzhou, encuentro con guía profesional de arte, introducción a la ruta de exploración artística del día.
157	52	es	Tour de Galerías	Visita múltiples galerías de arte moderno famosas, aprecia obras de arte contemporáneo chino, comprende tendencias de desarrollo artístico.
158	53	es	Exploración de Parque Creativo	Explora parques creativos famosos como Red Brick Factory, siente la colisión entre arquitectura industrial tradicional y arte moderno.
159	54	es	Estudio de Artista	Visita estudios de artistas activos, observa procesos creativos, intercambia cara a cara con artistas.
160	55	es	Resumen de Intercambio Cultural	Resume la experiencia del día en café artístico, comparte sentimientos sobre arte moderno de Guangzhou y cultura innovadora.
161	51	fr	Rassemblement dans le District Artistique	Rassemblement dans le district d'art moderne de Guangzhou, rencontre avec guide professionnel d'art, introduction à la route d'exploration artistique du jour.
162	52	fr	Tour des Galeries	Visitez plusieurs galeries d'art moderne célèbres, appréciez des œuvres d'art contemporain chinois, comprenez les tendances de développement artistique.
163	53	fr	Exploration du Parc Créatif	Explorez des parcs créatifs célèbres comme Red Brick Factory, ressentez la collision entre architecture industrielle traditionnelle et art moderne.
164	54	fr	Studio d'Artiste	Visitez des studios d'artistes actifs, observez les processus créatifs, échangez face à face avec des artistes.
165	55	fr	Résumé d'Échange Culturel	Résumez l'expérience du jour dans un café artistique, partagez sentiments sur l'art moderne de Guangzhou et culture innovante.
166	81	zh	创新之都欢迎	抵达赫尔辛基创新区，与创新生态专家导游见面，介绍芬兰创新历史和今日学习计划。
167	82	zh	创新中心参访	参观Maria 01等知名创新中心，了解芬兰创业支持体系和孵化模式。
168	83	zh	初创企业交流	与不同阶段的初创企业创始人交流，学习他们的创业经验和商业模式。
169	84	zh	投资人对话	与芬兰知名投资人对话，了解北欧投资环境和创业资本市场。
170	85	zh	创新文化体验	在创新空间体验芬兰独特的工作文化，总结创新生态系统的学习收获。
171	81	es	Bienvenida a la Capital de Innovación	Llegada al distrito de innovación de Helsinki, encuentro con guía experto en ecosistema de innovación, introducción a la historia de innovación finlandesa y plan de aprendizaje del día.
172	82	es	Visita a Centros de Innovación	Visita centros de innovación famosos como Maria 01, comprende el sistema de apoyo emprendedor finlandés y modelos de incubación.
173	83	es	Intercambio con Startups	Intercambia con fundadores de startups en diferentes etapas, aprende sus experiencias emprendedoras y modelos de negocio.
174	84	es	Diálogo con Inversionistas	Dialoga con inversionistas finlandeses famosos, comprende el ambiente de inversión nórdico y mercado de capital emprendedor.
175	85	es	Experiencia de Cultura Innovadora	Experimenta la cultura de trabajo única finlandesa en espacio de innovación, resume aprendizajes del ecosistema de innovación.
176	81	fr	Accueil à la Capitale d'Innovation	Arrivée au district d'innovation d'Helsinki, rencontre avec guide expert en écosystème d'innovation, introduction à l'histoire d'innovation finlandaise et plan d'apprentissage du jour.
177	82	fr	Visite des Centres d'Innovation	Visitez des centres d'innovation célèbres comme Maria 01, comprenez le système de soutien entrepreneurial finlandais et modèles d'incubation.
178	83	fr	Échange avec Startups	Échangez avec des fondateurs de startups à différentes étapes, apprenez leurs expériences entrepreneuriales et modèles d'affaires.
179	84	fr	Dialogue avec Investisseurs	Dialoguez avec des investisseurs finlandais célèbres, comprenez l'environnement d'investissement nordique et marché de capital entrepreneurial.
180	85	fr	Expérience de Culture Innovante	Vivez la culture de travail unique finlandaise dans l'espace d'innovation, résumez les apprentissages de l'écosystème d'innovation.
\.


--
-- TOC entry 4190 (class 0 OID 27064)
-- Dependencies: 236
-- Data for Name: activity_timelines; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activity_timelines (id, activity_id, step_number, title, description, duration_minutes, image_url, order_index) FROM stdin;
1	1	1	Meeting and Introduction	Meet your guide and group members, brief introduction to the day's activities	30	https://picsum.photos/seed/great-wall-private-tour-beijing-step-1-meeting-and-introduction/600/400	0
2	1	2	Journey Begins	Travel to the main destination with historical context and local insights	60	https://picsum.photos/seed/great-wall-private-tour-beijing-step-2-journey-begins/600/400	1
3	1	3	Main Experience	Explore the main attraction with detailed guided tour and photo opportunities	180	https://picsum.photos/seed/great-wall-private-tour-beijing-step-3-main-experience/600/400	2
4	1	4	Cultural Immersion	Experience local culture, traditions, or cuisine as part of the tour	90	https://picsum.photos/seed/great-wall-private-tour-beijing-step-4-cultural-immersion/600/400	3
5	1	5	Wrap-up and Return	Final questions, souvenir time, and comfortable return journey	60	https://picsum.photos/seed/great-wall-private-tour-beijing-step-5-wrap-up-and-return/600/400	4
6	2	1	Meeting and Introduction	Meet your guide and group members, brief introduction to the day's activities	30	https://picsum.photos/seed/shanghai-food-tour-street-food-step-1-meeting-and-introduction/600/400	0
7	2	2	Journey Begins	Travel to the main destination with historical context and local insights	60	https://picsum.photos/seed/shanghai-food-tour-street-food-step-2-journey-begins/600/400	1
8	2	3	Main Experience	Explore the main attraction with detailed guided tour and photo opportunities	180	https://picsum.photos/seed/shanghai-food-tour-street-food-step-3-main-experience/600/400	2
9	2	4	Cultural Immersion	Experience local culture, traditions, or cuisine as part of the tour	90	https://picsum.photos/seed/shanghai-food-tour-street-food-step-4-cultural-immersion/600/400	3
10	2	5	Wrap-up and Return	Final questions, souvenir time, and comfortable return journey	60	https://picsum.photos/seed/shanghai-food-tour-street-food-step-5-wrap-up-and-return/600/400	4
11	3	1	Meeting and Introduction	Meet your guide and group members, brief introduction to the day's activities	30	https://picsum.photos/seed/stockholm-university-study-tour-step-1-meeting-and-introduction/600/400	0
12	3	2	Journey Begins	Travel to the main destination with historical context and local insights	60	https://picsum.photos/seed/stockholm-university-study-tour-step-2-journey-begins/600/400	1
13	3	3	Main Experience	Explore the main attraction with detailed guided tour and photo opportunities	180	https://picsum.photos/seed/stockholm-university-study-tour-step-3-main-experience/600/400	2
14	3	4	Cultural Immersion	Experience local culture, traditions, or cuisine as part of the tour	90	https://picsum.photos/seed/stockholm-university-study-tour-step-4-cultural-immersion/600/400	3
15	3	5	Wrap-up and Return	Final questions, souvenir time, and comfortable return journey	60	https://picsum.photos/seed/stockholm-university-study-tour-step-5-wrap-up-and-return/600/400	4
16	4	1	Meeting and Introduction	Meet your guide and group members, brief introduction to the day's activities	30	https://picsum.photos/seed/copenhagen-design-academy-workshop-step-1-meeting-and-introduction/600/400	0
17	4	2	Journey Begins	Travel to the main destination with historical context and local insights	60	https://picsum.photos/seed/copenhagen-design-academy-workshop-step-2-journey-begins/600/400	1
18	4	3	Main Experience	Explore the main attraction with detailed guided tour and photo opportunities	180	https://picsum.photos/seed/copenhagen-design-academy-workshop-step-3-main-experience/600/400	2
19	4	4	Cultural Immersion	Experience local culture, traditions, or cuisine as part of the tour	90	https://picsum.photos/seed/copenhagen-design-academy-workshop-step-4-cultural-immersion/600/400	3
20	4	5	Wrap-up and Return	Final questions, souvenir time, and comfortable return journey	60	https://picsum.photos/seed/copenhagen-design-academy-workshop-step-5-wrap-up-and-return/600/400	4
21	5	1	Meeting and Introduction	Meet your guide and group members, brief introduction to the day's activities	30	https://picsum.photos/seed/oslo-northern-lights-arctic-culture-step-1-meeting-and-introduction/600/400	0
22	5	2	Journey Begins	Travel to the main destination with historical context and local insights	60	https://picsum.photos/seed/oslo-northern-lights-arctic-culture-step-2-journey-begins/600/400	1
23	5	3	Main Experience	Explore the main attraction with detailed guided tour and photo opportunities	180	https://picsum.photos/seed/oslo-northern-lights-arctic-culture-step-3-main-experience/600/400	2
24	5	4	Cultural Immersion	Experience local culture, traditions, or cuisine as part of the tour	90	https://picsum.photos/seed/oslo-northern-lights-arctic-culture-step-4-cultural-immersion/600/400	3
25	5	5	Wrap-up and Return	Final questions, souvenir time, and comfortable return journey	60	https://picsum.photos/seed/oslo-northern-lights-arctic-culture-step-5-wrap-up-and-return/600/400	4
26	6	1	Meeting and Introduction	Meet your guide and group members, brief introduction to the day's activities	30	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-step-1-meeting-and-introduction/600/400	0
27	6	2	Journey Begins	Travel to the main destination with historical context and local insights	60	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-step-2-journey-begins/600/400	1
28	6	3	Main Experience	Explore the main attraction with detailed guided tour and photo opportunities	180	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-step-3-main-experience/600/400	2
29	6	4	Cultural Immersion	Experience local culture, traditions, or cuisine as part of the tour	90	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-step-4-cultural-immersion/600/400	3
30	6	5	Wrap-up and Return	Final questions, souvenir time, and comfortable return journey	60	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-step-5-wrap-up-and-return/600/400	4
36	8	1	Meet & Greet	Meet your guide and fellow participants, brief introduction	30	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-timeline-1/600/400	0
37	8	2	Journey Begins	Travel to main location with background information	60	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-timeline-2/600/400	1
38	8	3	Main Experience	Core activity with hands-on participation	180	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-timeline-3/600/400	2
39	8	4	Cultural Immersion	Deep dive into local culture and traditions	90	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-timeline-4/600/400	3
40	8	5	Wrap-up	Final discussions, photos, and return journey	60	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-timeline-5/600/400	4
41	9	1	Meet & Greet	Meet your guide and fellow participants, brief introduction	30	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-timeline-1/600/400	0
42	9	2	Journey Begins	Travel to main location with background information	60	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-timeline-2/600/400	1
43	9	3	Main Experience	Core activity with hands-on participation	180	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-timeline-3/600/400	2
44	9	4	Cultural Immersion	Deep dive into local culture and traditions	90	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-timeline-4/600/400	3
45	9	5	Wrap-up	Final discussions, photos, and return journey	60	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-timeline-5/600/400	4
46	10	1	Meet & Greet	Meet your guide and fellow participants, brief introduction	30	https://picsum.photos/seed/beijing-traditional-arts-temple-culture-timeline-1/600/400	0
47	10	2	Journey Begins	Travel to main location with background information	60	https://picsum.photos/seed/beijing-traditional-arts-temple-culture-timeline-2/600/400	1
48	10	3	Main Experience	Core activity with hands-on participation	180	https://picsum.photos/seed/beijing-traditional-arts-temple-culture-timeline-3/600/400	2
49	10	4	Cultural Immersion	Deep dive into local culture and traditions	90	https://picsum.photos/seed/beijing-traditional-arts-temple-culture-timeline-4/600/400	3
50	10	5	Wrap-up	Final discussions, photos, and return journey	60	https://picsum.photos/seed/beijing-traditional-arts-temple-culture-timeline-5/600/400	4
51	11	1	Meet & Greet	Meet your guide and fellow participants, brief introduction	30	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-timeline-1/600/400	0
52	11	2	Journey Begins	Travel to main location with background information	60	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-timeline-2/600/400	1
53	11	3	Main Experience	Core activity with hands-on participation	180	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-timeline-3/600/400	2
54	11	4	Cultural Immersion	Deep dive into local culture and traditions	90	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-timeline-4/600/400	3
55	11	5	Wrap-up	Final discussions, photos, and return journey	60	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-timeline-5/600/400	4
56	12	1	Meet & Greet	Meet your guide and fellow participants, brief introduction	30	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-timeline-1/600/400	0
57	12	2	Journey Begins	Travel to main location with background information	60	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-timeline-2/600/400	1
58	12	3	Main Experience	Core activity with hands-on participation	180	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-timeline-3/600/400	2
59	12	4	Cultural Immersion	Deep dive into local culture and traditions	90	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-timeline-4/600/400	3
60	12	5	Wrap-up	Final discussions, photos, and return journey	60	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-timeline-5/600/400	4
61	13	1	Meet & Greet	Meet your guide and fellow participants, brief introduction	30	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-timeline-1/600/400	0
62	13	2	Journey Begins	Travel to main location with background information	60	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-timeline-2/600/400	1
63	13	3	Main Experience	Core activity with hands-on participation	180	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-timeline-3/600/400	2
64	13	4	Cultural Immersion	Deep dive into local culture and traditions	90	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-timeline-4/600/400	3
65	13	5	Wrap-up	Final discussions, photos, and return journey	60	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-timeline-5/600/400	4
66	14	1	Meet & Greet	Meet your guide and fellow participants, brief introduction	30	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-timeline-1/600/400	0
67	14	2	Journey Begins	Travel to main location with background information	60	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-timeline-2/600/400	1
68	14	3	Main Experience	Core activity with hands-on participation	180	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-timeline-3/600/400	2
69	14	4	Cultural Immersion	Deep dive into local culture and traditions	90	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-timeline-4/600/400	3
70	14	5	Wrap-up	Final discussions, photos, and return journey	60	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-timeline-5/600/400	4
71	15	1	Meet & Greet	Meet your guide and fellow participants, brief introduction	30	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-timeline-1/600/400	0
72	15	2	Journey Begins	Travel to main location with background information	60	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-timeline-2/600/400	1
73	15	3	Main Experience	Core activity with hands-on participation	180	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-timeline-3/600/400	2
74	15	4	Cultural Immersion	Deep dive into local culture and traditions	90	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-timeline-4/600/400	3
75	15	5	Wrap-up	Final discussions, photos, and return journey	60	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-timeline-5/600/400	4
76	16	1	Meet & Greet	Meet your guide and fellow participants, brief introduction	30	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-timeline-1/600/400	0
77	16	2	Journey Begins	Travel to main location with background information	60	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-timeline-2/600/400	1
78	16	3	Main Experience	Core activity with hands-on participation	180	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-timeline-3/600/400	2
79	16	4	Cultural Immersion	Deep dive into local culture and traditions	90	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-timeline-4/600/400	3
80	16	5	Wrap-up	Final discussions, photos, and return journey	60	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-timeline-5/600/400	4
81	17	1	Meet & Greet	Meet your guide and fellow participants, brief introduction	30	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-timeline-1/600/400	0
82	17	2	Journey Begins	Travel to main location with background information	60	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-timeline-2/600/400	1
83	17	3	Main Experience	Core activity with hands-on participation	180	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-timeline-3/600/400	2
84	17	4	Cultural Immersion	Deep dive into local culture and traditions	90	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-timeline-4/600/400	3
85	17	5	Wrap-up	Final discussions, photos, and return journey	60	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-timeline-5/600/400	4
86	18	1	Meet & Greet	Meet your guide and fellow participants, brief introduction	30	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-timeline-1/600/400	0
87	18	2	Journey Begins	Travel to main location with background information	60	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-timeline-2/600/400	1
88	18	3	Main Experience	Core activity with hands-on participation	180	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-timeline-3/600/400	2
89	18	4	Cultural Immersion	Deep dive into local culture and traditions	90	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-timeline-4/600/400	3
90	18	5	Wrap-up	Final discussions, photos, and return journey	60	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-timeline-5/600/400	4
91	19	1	Meet & Greet	Meet your guide and fellow participants, brief introduction	30	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-timeline-1/600/400	0
92	19	2	Journey Begins	Travel to main location with background information	60	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-timeline-2/600/400	1
93	19	3	Main Experience	Core activity with hands-on participation	180	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-timeline-3/600/400	2
94	19	4	Cultural Immersion	Deep dive into local culture and traditions	90	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-timeline-4/600/400	3
95	19	5	Wrap-up	Final discussions, photos, and return journey	60	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-timeline-5/600/400	4
96	20	1	Meet & Greet	Meet your guide and fellow participants, brief introduction	30	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-timeline-1/600/400	0
97	20	2	Journey Begins	Travel to main location with background information	60	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-timeline-2/600/400	1
98	20	3	Main Experience	Core activity with hands-on participation	180	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-timeline-3/600/400	2
99	20	4	Cultural Immersion	Deep dive into local culture and traditions	90	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-timeline-4/600/400	3
100	20	5	Wrap-up	Final discussions, photos, and return journey	60	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-timeline-5/600/400	4
101	21	1	Meet & Greet	Meet your guide and fellow participants, brief introduction	30	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-timeline-1/600/400	0
102	21	2	Journey Begins	Travel to main location with background information	60	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-timeline-2/600/400	1
103	21	3	Main Experience	Core activity with hands-on participation	180	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-timeline-3/600/400	2
104	21	4	Cultural Immersion	Deep dive into local culture and traditions	90	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-timeline-4/600/400	3
105	21	5	Wrap-up	Final discussions, photos, and return journey	60	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-timeline-5/600/400	4
106	22	1	Meet & Greet	Meet your guide and fellow participants, brief introduction	30	https://picsum.photos/seed/stockholm-modern-design-architecture-walking-tour-timeline-1/600/400	0
107	22	2	Journey Begins	Travel to main location with background information	60	https://picsum.photos/seed/stockholm-modern-design-architecture-walking-tour-timeline-2/600/400	1
108	22	3	Main Experience	Core activity with hands-on participation	180	https://picsum.photos/seed/stockholm-modern-design-architecture-walking-tour-timeline-3/600/400	2
109	22	4	Cultural Immersion	Deep dive into local culture and traditions	90	https://picsum.photos/seed/stockholm-modern-design-architecture-walking-tour-timeline-4/600/400	3
110	22	5	Wrap-up	Final discussions, photos, and return journey	60	https://picsum.photos/seed/stockholm-modern-design-architecture-walking-tour-timeline-5/600/400	4
\.


--
-- TOC entry 4203 (class 0 OID 27183)
-- Dependencies: 249
-- Data for Name: activity_translations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activity_translations (id, activity_id, language, title, short_description, description, dress_code, what_to_bring, not_suitable_for, covid_measures, cancellation_policy, created_at, updated_at) FROM stdin;
1	1	zh	北京长城私人一日游含午餐	在专业导游陪同下探索雄伟的慕田峪长城，享用传统中式午餐	在这次长城私人游中体验世界最著名的地标之一。参观保存完好的慕田峪段，以其壮美的山景和较少的游客而闻名。专业当地导游将分享这个联合国教科文组织世界遗产的迷人故事，同时您漫步在古老的城墙上。包含往返交通、缆车票和正宗中式午餐。	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
2	1	es	Tour Privado de un Día a la Gran Muralla China con Almuerzo	Explora la magnífica Gran Muralla en la sección Mutianyu con guía privado y almuerzo chino tradicional	Experimenta uno de los monumentos más icónicos del mundo en este tour privado de la Gran Muralla. Visita la sección bien conservada de Mutianyu, conocida por su impresionante paisaje montañoso y menos multitudes. Tu guía local experto compartirá historias fascinantes sobre este sitio del Patrimonio Mundial de la UNESCO mientras caminas por las murallas antiguas. Incluye transporte de ida y vuelta, boletos de teleférico y auténtico almuerzo chino.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
3	1	fr	Visite Privée d'une Journée à la Grande Muraille de Chine avec Déjeuner	Explorez la magnifique Grande Muraille à la section Mutianyu avec un guide privé et un déjeuner chinois traditionnel	Découvrez l'un des monuments les plus emblématiques du monde lors de cette visite privée de la Grande Muraille. Visitez la section bien préservée de Mutianyu, connue pour ses paysages de montagne époustouflants et moins de foules. Votre guide local expert partagera des histoires fascinantes sur ce site du patrimoine mondial de l'UNESCO pendant que vous marchez le long des murs anciens. Transport aller-retour, billets de téléphérique et déjeuner chinois authentique inclus.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
4	3	zh	斯德哥尔摩大学校园与瑞典教育体系游学之旅	通过大学参观、学生交流和教育洞察探索瑞典高等教育体系	在这次全面的游学之旅中深入了解享誉世界的瑞典教育体系。参观斯德哥尔摩大学校园，与国际学生和教授会面，了解瑞典创新的高等教育方法。非常适合学生、教育工作者和任何对北欧教育卓越感兴趣的人。	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
5	3	es	Tour de Estudio del Campus Universitario de Estocolmo y Sistema Educativo Sueco	Explora el sistema de educación superior sueco con visitas universitarias, interacciones estudiantiles y perspectivas educativas	Sumérgete en el reconocido sistema educativo sueco en este tour de estudio integral. Visita el campus de la Universidad de Estocolmo, conoce estudiantes internacionales y profesores, y aprende sobre el enfoque innovador de Suecia hacia la educación superior. Perfecto para estudiantes, educadores y cualquiera interesado en la excelencia educativa nórdica.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
6	2	zh	上海美食之旅：当地街头美食与隐藏宝藏	在导游带领下通过当地市场和街头摊位发现正宗上海风味	踏上穿越上海充满活力的美食场景的烹饪冒险之旅。这次导游之旅带您远离游客餐厅，发现正宗的当地风味。参观繁忙的湿货市场、历史悠久的美食街和只有当地人知道的隐藏宝藏。品尝传统菜肴如小笼包、生煎包和其他上海特色美食。	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
7	2	es	Tour Gastronómico de Shanghái: Comida Callejera Local y Joyas Ocultas	Descubre auténticos sabores de Shanghái en este tour gastronómico guiado por mercados locales y puestos de comida callejera	Embárcate en una aventura culinaria a través de la vibrante escena gastronómica de Shanghái. Este tour guiado te lleva más allá de los restaurantes turísticos para descubrir sabores locales auténticos. Visita mercados húmedos bulliciosos, calles de comida históricas y joyas ocultas conocidas solo por los locales. Prueba platos tradicionales como xiaolongbao y shengjianbao.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
10	4	zh	哥本哈根设计学院与丹麦设计哲学工作坊	通过学院参观、实践工作坊和设计师会面学习丹麦设计原则	在这次沉浸式教育体验中发现丹麦世界著名设计哲学的秘密。参观丹麦设计学院，参加实践工作坊，与专业设计师会面。了解hygge、功能性和定义丹麦设计的极简主义。这次游学之旅将理论知识与实践经验相结合，非常适合设计学生、专业人士和爱好者。	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
11	4	es	Academia de Diseño de Copenhague y Taller de Filosofía del Diseño Danés	Aprende los principios del diseño danés a través de visitas a la academia, talleres prácticos y reuniones con diseñadores	Descubre los secretos detrás de la filosofía de diseño mundialmente reconocida de Dinamarca en esta experiencia educativa inmersiva. Visita la Academia de Diseño Danés, participa en talleres prácticos y conoce a diseñadores profesionales. Aprende sobre hygge, funcionalidad y minimalismo que definen el diseño danés. Este tour de estudio combina conocimiento teórico con experiencia práctica, perfecto para estudiantes de diseño, profesionales y entusiastas.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
12	4	fr	Académie de Design de Copenhague et Atelier de Philosophie du Design Danois	Apprenez les principes du design danois à travers des visites d'académie, des ateliers pratiques et des rencontres avec des designers	Découvrez les secrets derrière la philosophie de design mondialement reconnue du Danemark dans cette expérience éducative immersive. Visitez l'Académie de Design Danois, participez à des ateliers pratiques et rencontrez des designers professionnels. Apprenez sur le hygge, la fonctionnalité et le minimalisme qui définissent le design danois. Cette visite d'étude combine connaissances théoriques et expérience pratique, parfaite pour les étudiants en design, les professionnels et les passionnés.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
16	16	zh	奥斯陆大学可持续发展与绿色技术学习项目	向挪威领先的可持续发展专家学习奥斯陆大学环境项目	通过奥斯陆大学的这个综合学习项目，沉浸在挪威在可持续发展和绿色技术方面的开创性方法中。与从事气候解决方案工作的教授和研究人员会面，参观尖端实验室，参与可再生能源和环境政策研讨会，了解挪威如何在可持续发展方面引领世界。	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
17	16	es	Programa de Estudio de Sostenibilidad y Tecnología Verde de la Universidad de Oslo	Aprende de los expertos líderes en sostenibilidad de Noruega en los programas ambientales de la Universidad de Oslo	Sumérgete en el enfoque pionero de Noruega hacia la sostenibilidad y la tecnología verde a través de este programa de estudio integral en la Universidad de Oslo. Conoce a profesores e investigadores que trabajan en soluciones climáticas, visita laboratorios de vanguardia, participa en talleres sobre energía renovable y política ambiental, y comprende cómo Noruega lidera el mundo en desarrollo sostenible.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
38	17	es	Tour de Estudio del Hub de Innovación y Ecosistema de Startups Finlandés	Comprende profundamente el ecosistema de innovación líder de Finlandia, visita startups famosas y centros tecnológicos	Explora los secretos del éxito de Finlandia como potencia global de innovación. Visita centros de innovación de Helsinki, incubadoras de startups y empresas tecnológicas, intercambia con emprendedores e inversionistas, aprende metodologías de innovación únicas finlandesas y modelos de negocio. Comprende cómo la cultura de innovación nórdica ha dado origen a numerosas empresas tecnológicas exitosas.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
18	16	fr	Programme d'Étude de Durabilité et Technologie Verte de l'Université d'Oslo	Apprenez auprès des experts en durabilité leaders de la Norvège dans les programmes environnementaux de l'Université d'Oslo	Plongez dans l'approche pionnière de la Norvège vers la durabilité et la technologie verte à travers ce programme d'étude complet à l'Université d'Oslo. Rencontrez des professeurs et chercheurs travaillant sur les solutions climatiques, visitez des laboratoires de pointe, participez à des ateliers sur l'énergie renouvelable et la politique environnementale, et comprenez comment la Norvège mène le monde en développement durable.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
19	20	zh	挪威峡湾与北极野生动物摄影探险	在这次摄影探险中捕捉挪威峡湾和北极野生动物的原始之美	踏上穿越挪威最壮观峡湾和北极地区的难忘摄影探险之旅。向专业野生动物摄影师学习，同时拍摄海豹、鲸鱼、北极鸟类和挪威海岸戏剧性景观的图像。根据季节体验午夜太阳或北极光，掌握极端天气摄影技巧。	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
20	20	es	Expedición Fotográfica de Fiordos Noruegos y Vida Silvestre Ártica	Captura la belleza cruda de los fiordos noruegos y la vida silvestre ártica en esta expedición fotográfica	Embárcate en una expedición fotográfica inolvidable a través de los fiordos más espectaculares de Noruega y regiones árticas. Aprende de fotógrafos profesionales de vida silvestre mientras capturas imágenes de focas, ballenas, aves árticas y los paisajes dramáticos de la costa noruega. Experimenta el sol de medianoche o las auroras boreales dependiendo de la temporada, y domina técnicas para fotografía en clima extremo.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
21	20	fr	Expédition Photographique des Fjords Norvégiens et de la Faune Arctique	Capturez la beauté brute des fjords norvégiens et de la faune arctique lors de cette expédition photographique	Embarquez pour une expédition photographique inoubliable à travers les fjords les plus spectaculaires de Norvège et les régions arctiques. Apprenez auprès de photographes professionnels de la faune tout en capturant des images de phoques, baleines, oiseaux arctiques et les paysages dramatiques de la côte norvégienne. Vivez le soleil de minuit ou les aurores boréales selon la saison, et maîtrisez les techniques de photographie par temps extrême.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
8	2	fr	Tour Gastronomique de Shanghai : Street Food Locale et Trésors Cachés	Découvrez les saveurs authentiques de Shanghai lors de ce tour gastronomique guidé à travers les marchés locaux et les stands de street food	Embarquez pour une aventure culinaire à travers la scène gastronomique dynamique de Shanghai. Ce tour guidé vous emmène au-delà des restaurants touristiques pour découvrir des saveurs locales authentiques. Visitez des marchés animés, des rues de nourriture historiques et des trésors cachés connus seulement des locaux. Goûtez des plats traditionnels comme les xiaolongbao et shengjianbao.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
9	3	fr	Visite d'Étude du Campus Universitaire de Stockholm et du Système Éducatif Suédois	Explorez le système d'enseignement supérieur suédois avec des visites d'université, des interactions étudiantes et des perspectives éducatives	Plongez dans le système éducatif suédois renommé lors de cette visite d'étude complète. Visitez le campus de l'Université de Stockholm, rencontrez des étudiants internationaux et des professeurs, et découvrez l'approche innovante de la Suède envers l'enseignement supérieur. Parfait pour les étudiants, les éducateurs et toute personne intéressée par l'excellence éducative nordique.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
13	8	zh	四川烹饪学院大师烹饪课	在成都顶级烹饪学院向专业厨师学习正宗川菜	在成都著名烹饪学院的这次全面烹饪大师班中，沉浸在火辣的川菜世界里。向经过认证的川菜厨师学习制作传统菜肴如麻婆豆腐、宫保鸡丁和担担面。了解平衡著名'麻辣'口味的艺术，在当地市场采购食材。	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
14	8	es	Clase Magistral de Cocina del Instituto Culinario de Sichuan	Aprende cocina auténtica de Sichuan de chefs profesionales en el instituto culinario premier de Chengdu	Sumérgete en el mundo ardiente de la cocina de Sichuan con esta clase magistral integral en el renombrado instituto culinario de Chengdu. Aprende a preparar platos tradicionales como Mapo Tofu, Pollo Kung Pao y Fideos Dan Dan de chefs certificados de Sichuan. Comprende el arte de equilibrar los famosos sabores 'mala' y abastécete de ingredientes en mercados locales.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
15	8	fr	Cours de Maître de Cuisine de l'Institut Culinaire du Sichuan	Apprenez la cuisine authentique du Sichuan auprès de chefs professionnels dans l'institut culinaire premier de Chengdu	Plongez dans le monde ardent de la cuisine du Sichuan avec ce cours de maître complet dans l'institut culinaire renommé de Chengdu. Apprenez à préparer des plats traditionnels comme le Mapo Tofu, le Poulet Kung Pao et les Nouilles Dan Dan auprès de chefs certifiés du Sichuan. Comprenez l'art d'équilibrer les saveurs 'mala' célèbres et approvisionnez-vous en ingrédients sur les marchés locaux.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
22	6	zh	西安兵马俑发现之旅与古代历史	探索令人惊叹的兵马俑博物馆，深入了解中国古代历史和秦朝文化	踏上一场穿越时间的非凡旅程，探索世界第八大奇迹兵马俑。在这次综合历史之旅中，您将发现数千个真人大小的陶制士兵、马匹和战车，每个都有独特的面部特征和细节。了解秦始皇的传奇故事和中国古代文明。	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
23	6	es	Tour de Descubrimiento del Ejército de Terracota de Xi'an con Historia Antigua	Explora el impresionante Museo del Ejército de Terracota y sumérgete profundamente en la historia china antigua y la cultura de la Dinastía Qin	Embárcate en un viaje extraordinario a través del tiempo para explorar la Octava Maravilla del Mundo, el Ejército de Terracota. En este tour histórico integral, descubrirás miles de soldados, caballos y carros de arcilla de tamaño real, cada uno con características faciales y detalles únicos. Aprende sobre la historia legendaria del Emperador Qin Shi Huang y la civilización china antigua.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
24	6	fr	Tour de Découverte de l'Armée de Terre Cuite de Xi'an avec Histoire Ancienne	Explorez l'impressionnant Musée de l'Armée de Terre Cuite et plongez profondément dans l'histoire chinoise ancienne et la culture de la Dynastie Qin	Embarquez pour un voyage extraordinaire à travers le temps pour explorer la Huitième Merveille du Monde, l'Armée de Terre Cuite. Dans ce tour historique complet, vous découvrirez des milliers de soldats, chevaux et chars en argile grandeur nature, chacun avec des traits faciaux et des détails uniques. Apprenez l'histoire légendaire de l'Empereur Qin Shi Huang et la civilisation chinoise ancienne.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
25	5	zh	北极光追踪与北极文化体验	在北极圈内追寻神秘的北极光，深入体验萨米族传统文化和北极生活方式	踏上一场寻找地球上最壮观自然现象之一的冒险之旅。在经验丰富的北极导游带领下，您将学习预测北极光的科学知识，体验萨米族的传统文化，包括驯鹿放牧、传统手工艺和古老的生存技巧。享受北极地区的独特住宿和当地美食。	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
26	5	es	Persecución de Auroras Boreales y Experiencia Cultural Ártica	Persigue las misteriosas auroras boreales en el Círculo Ártico y experimenta profundamente la cultura tradicional Sami y el estilo de vida ártico	Embárcate en una aventura para encontrar uno de los fenómenos naturales más espectaculares de la Tierra. Bajo la guía de un guía ártico experimentado, aprenderás la ciencia de predecir auroras boreales, experimentarás la cultura tradicional Sami, incluyendo pastoreo de renos, artesanías tradicionales y técnicas ancestrales de supervivencia. Disfruta del alojamiento único de la región ártica y la cocina local.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
27	5	fr	Chasse aux Aurores Boréales et Expérience Culturelle Arctique	Poursuivez les mystérieuses aurores boréales dans le Cercle Arctique et vivez profondément la culture traditionnelle Sami et le mode de vie arctique	Embarquez pour une aventure à la recherche de l'un des phénomènes naturels les plus spectaculaires de la Terre. Sous la guidance d'un guide arctique expérimenté, vous apprendrez la science de prédiction des aurores boréales, vivrez la culture traditionnelle Sami, incluant l'élevage de rennes, l'artisanat traditionnel et les techniques anciennes de survie. Profitez de l'hébergement unique de la région arctique et de la cuisine locale.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
28	9	zh	张家界阿凡达山脉摄影探险	在张家界国家森林公园拍摄电影阿凡达的取景地，捕捉壮丽的石英砂岩峰林景观	探索激发詹姆斯·卡梅隆电影《阿凡达》创作的神奇山景。在专业摄影师指导下，您将学习如何拍摄这些独特的石英砂岩柱和云雾缭绕的峰林。乘坐世界最高的户外电梯，体验玻璃桥的刺激，在最佳摄影点捕捉令人屏息的自然美景。	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
29	9	es	Aventura Fotográfica de las Montañas Avatar de Zhangjiajie	Fotografía los lugares de filmación de Avatar en el Parque Nacional Forestal de Zhangjiajie, captura el magnífico paisaje de pilares de arenisca de cuarzo	Explora los paisajes montañosos mágicos que inspiraron la película 'Avatar' de James Cameron. Bajo la guía de fotógrafos profesionales, aprenderás cómo fotografiar estos únicos pilares de arenisca de cuarzo y bosques de picos envueltos en niebla. Toma el ascensor exterior más alto del mundo, experimenta la emoción del puente de cristal y captura la impresionante belleza natural en los mejores puntos fotográficos.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
30	9	fr	Aventure Photographique des Montagnes Avatar de Zhangjiajie	Photographiez les lieux de tournage d'Avatar dans le Parc National Forestier de Zhangjiajie, capturez le magnifique paysage de piliers de grès de quartz	Explorez les paysages montagneux magiques qui ont inspiré le film 'Avatar' de James Cameron. Sous la guidance de photographes professionnels, vous apprendrez comment photographier ces piliers uniques de grès de quartz et forêts de pics enveloppées de brouillard. Prenez l'ascenseur extérieur le plus haut du monde, vivez l'excitation du pont de verre et capturez la beauté naturelle époustouflante aux meilleurs points photographiques.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
31	10	zh	北京传统艺术与寺庙文化体验	深入体验北京古老的传统艺术和寺庙文化，学习书法、国画等传统技艺	在这次深度文化体验中，您将探索北京丰富的传统艺术遗产和古老的寺庙文化。参访历史悠久的寺庙，学习中国传统艺术如书法、国画、剪纸等，与当地艺术家交流，了解这些艺术形式的历史意义和现代传承。	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
32	10	es	Experiencia de Artes Tradicionales y Cultura de Templos de Beijing	Experimenta profundamente las artes tradicionales antiguas y cultura de templos de Beijing, aprende caligrafía, pintura tradicional china y otras habilidades tradicionales	En esta experiencia cultural profunda, explorarás el rico patrimonio artístico tradicional de Beijing y la antigua cultura de templos. Visita templos históricos, aprende artes tradicionales chinas como caligrafía, pintura china, papel cortado, etc., intercambia con artistas locales y comprende el significado histórico y herencia moderna de estas formas artísticas.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
33	10	fr	Expérience des Arts Traditionnels et Culture des Temples de Beijing	Vivez profondément les arts traditionnels anciens et la culture des temples de Beijing, apprenez calligraphie, peinture chinoise traditionnelle et autres compétences traditionnelles	Dans cette expérience culturelle profonde, vous explorerez le riche patrimoine artistique traditionnel de Beijing et l'ancienne culture des temples. Visitez des temples historiques, apprenez les arts traditionnels chinois comme la calligraphie, peinture chinoise, découpage de papier, etc., échangez avec des artistes locaux et comprenez la signification historique et l'héritage moderne de ces formes artistiques.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
34	11	zh	广州现代艺术与创新区域游览	探索广州充满活力的现代艺术场景，参访创新园区和当代艺术画廊	发现广州作为中国南方艺术和创新中心的独特魅力。参观现代艺术画廊、创意园区和设计工作室，与当地艺术家交流，了解广州当代艺术的发展和创新文化的繁荣。体验传统岭南文化与现代创意的完美结合。	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
35	11	es	Tour del Distrito de Arte Moderno e Innovación de Guangzhou	Explora la vibrante escena de arte moderno de Guangzhou, visita parques de innovación y galerías de arte contemporáneo	Descubre el encanto único de Guangzhou como centro de arte e innovación del sur de China. Visita galerías de arte moderno, parques creativos y estudios de diseño, intercambia con artistas locales, comprende el desarrollo del arte contemporáneo de Guangzhou y la prosperidad de la cultura innovadora. Experimenta la perfecta combinación de la cultura tradicional Lingnan con la creatividad moderna.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
36	11	fr	Tour du District d'Art Moderne et d'Innovation de Guangzhou	Explorez la scène artistique moderne vibrante de Guangzhou, visitez des parcs d'innovation et galeries d'art contemporain	Découvrez le charme unique de Guangzhou en tant que centre d'art et d'innovation du sud de la Chine. Visitez des galeries d'art moderne, parcs créatifs et studios de design, échangez avec des artistes locaux, comprenez le développement de l'art contemporain de Guangzhou et la prospérité de la culture innovante. Vivez la combinaison parfaite de la culture traditionnelle Lingnan avec la créativité moderne.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
37	17	zh	芬兰创新中心与初创生态系统游学之旅	深入了解芬兰领先的创新生态系统，参访知名初创企业和技术中心	探索芬兰作为全球创新强国的成功秘诀。参访赫尔辛基的创新中心、初创企业孵化器和技术公司，与创业者和投资人交流，学习芬兰独特的创新方法论和商业模式。了解北欧创新文化如何孕育出众多成功的科技企业。	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
39	17	fr	Tour d'Étude du Hub d'Innovation et Écosystème de Startups Finlandais	Comprenez profondément l'écosystème d'innovation leader de Finlande, visitez des startups célèbres et centres technologiques	Explorez les secrets du succès de la Finlande en tant que puissance mondiale d'innovation. Visitez des centres d'innovation d'Helsinki, incubateurs de startups et entreprises technologiques, échangez avec des entrepreneurs et investisseurs, apprenez les méthodologies d'innovation uniques finlandaises et modèles d'affaires. Comprenez comment la culture d'innovation nordique a donné naissance à de nombreuses entreprises technologiques réussies.	\N	\N	\N	\N	\N	2025-11-03 21:57:05.30544+02	\N
\.


--
-- TOC entry 4200 (class 0 OID 27152)
-- Dependencies: 246
-- Data for Name: availability; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.availability (id, activity_id, date, start_time, end_time, spots_available, spots_total, price_adult, price_child, is_available) FROM stdin;
\.


--
-- TOC entry 4198 (class 0 OID 27122)
-- Dependencies: 244
-- Data for Name: bookings; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.bookings (id, booking_ref, user_id, activity_id, vendor_id, booking_date, booking_time, adults, children, total_participants, price_per_adult, price_per_child, total_price, currency, status, customer_name, customer_email, customer_phone, special_requirements, rejection_reason, created_at, confirmed_at, vendor_approved_at, vendor_rejected_at, cancelled_at, completed_at) FROM stdin;
\.


--
-- TOC entry 4207 (class 0 OID 27216)
-- Dependencies: 253
-- Data for Name: cart_items; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cart_items (id, session_id, activity_id, booking_date, booking_time, adults, children, price, time_slot_id, pricing_tier_id, add_on_ids, add_on_quantities, created_at) FROM stdin;
\.


--
-- TOC entry 4166 (class 0 OID 26864)
-- Dependencies: 212
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.categories (id, name, slug, icon, parent_id, order_index) FROM stdin;
1	Tours	tours	🚌	\N	1
2	Food & Drink	food-drink	🍜	\N	2
3	Museums & Culture	museums	🏛️	\N	3
4	Outdoor Activities	outdoor	🏔️	\N	4
6	Adventure	adventure	🧗	\N	6
7	Luxury Experiences	luxury	💎	\N	7
8	Family-Friendly	family	👨‍👩‍👧‍👦	\N	8
9	Historical Sites	historical	🏺	\N	9
10	Nature & Wildlife	nature	🦌	\N	10
5	Study Tours	study-tours	📚	\N	5
\.


--
-- TOC entry 4172 (class 0 OID 26908)
-- Dependencies: 218
-- Data for Name: category_translations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.category_translations (id, category_id, language, name, created_at, updated_at) FROM stdin;
1	1	zh	观光游览	2025-11-04 11:01:24.384068+02	\N
2	1	es	Tours y Excursiones	2025-11-04 11:01:24.384068+02	\N
3	1	fr	Visites et Excursions	2025-11-04 11:01:24.384068+02	\N
4	2	zh	美食餐饮	2025-11-04 11:01:24.384068+02	\N
5	2	es	Comida y Bebida	2025-11-04 11:01:24.384068+02	\N
6	2	fr	Nourriture et Boissons	2025-11-04 11:01:24.384068+02	\N
7	3	zh	博物馆文化	2025-11-04 11:01:24.384068+02	\N
8	3	es	Museos y Cultura	2025-11-04 11:01:24.384068+02	\N
9	3	fr	Musées et Culture	2025-11-04 11:01:24.384068+02	\N
10	4	zh	户外活动	2025-11-04 11:01:24.384068+02	\N
11	4	es	Actividades al Aire Libre	2025-11-04 11:01:24.384068+02	\N
12	4	fr	Activités de Plein Air	2025-11-04 11:01:24.384068+02	\N
13	6	zh	冒险探险	2025-11-04 11:01:24.384068+02	\N
14	6	es	Aventura	2025-11-04 11:01:24.384068+02	\N
15	6	fr	Aventure	2025-11-04 11:01:24.384068+02	\N
16	7	zh	奢华体验	2025-11-04 11:01:24.384068+02	\N
17	7	es	Experiencias de Lujo	2025-11-04 11:01:24.384068+02	\N
18	7	fr	Expériences de Luxe	2025-11-04 11:01:24.384068+02	\N
19	8	zh	亲子友好	2025-11-04 11:01:24.384068+02	\N
20	8	es	Familiar	2025-11-04 11:01:24.384068+02	\N
21	8	fr	Adapté aux Familles	2025-11-04 11:01:24.384068+02	\N
22	9	zh	历史古迹	2025-11-04 11:01:24.384068+02	\N
23	9	es	Sitios Históricos	2025-11-04 11:01:24.384068+02	\N
24	9	fr	Sites Historiques	2025-11-04 11:01:24.384068+02	\N
25	10	zh	自然野生动物	2025-11-04 11:01:24.384068+02	\N
26	10	es	Naturaleza y Vida Silvestre	2025-11-04 11:01:24.384068+02	\N
27	10	fr	Nature et Faune	2025-11-04 11:01:24.384068+02	\N
28	5	zh	学习游学	2025-11-04 11:01:24.384068+02	\N
29	5	es	Tours de Estudio	2025-11-04 11:01:24.384068+02	\N
30	5	fr	Voyages d'Études	2025-11-04 11:01:24.384068+02	\N
\.


--
-- TOC entry 4174 (class 0 OID 26924)
-- Dependencies: 220
-- Data for Name: destination_translations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.destination_translations (id, destination_id, language, name, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 4168 (class 0 OID 26878)
-- Dependencies: 214
-- Data for Name: destinations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.destinations (id, name, slug, country, country_code, image_url, latitude, longitude, is_featured, created_at) FROM stdin;
1	Beijing	beijing	China	CN	https://picsum.photos/seed/destination-beijing/1200/800	39.9042	116.4074	t	2025-11-03 16:32:47.916739+02
2	Shanghai	shanghai	China	CN	https://picsum.photos/seed/destination-shanghai/1200/800	31.2304	121.4737	t	2025-11-03 16:32:47.916739+02
3	Xi'an	xian	China	CN	https://picsum.photos/seed/destination-xian/1200/800	34.3416	108.9398	f	2025-11-03 16:32:47.916739+02
4	Guilin	guilin	China	CN	https://picsum.photos/seed/destination-guilin/1200/800	25.274	110.29	f	2025-11-03 16:32:47.916739+02
5	Chengdu	chengdu	China	CN	https://picsum.photos/seed/destination-chengdu/1200/800	30.5728	104.0668	f	2025-11-03 16:32:47.916739+02
6	Hangzhou	hangzhou	China	CN	https://picsum.photos/seed/destination-hangzhou/1200/800	30.2741	120.1551	f	2025-11-03 16:32:47.916739+02
7	Stockholm	stockholm	Sweden	SE	https://picsum.photos/seed/destination-stockholm/1200/800	59.3293	18.0686	t	2025-11-03 16:32:47.916739+02
8	Copenhagen	copenhagen	Denmark	DK	https://picsum.photos/seed/destination-copenhagen/1200/800	55.6761	12.5683	t	2025-11-03 16:32:47.916739+02
9	Oslo	oslo	Norway	NO	https://picsum.photos/seed/destination-oslo/1200/800	59.9139	10.7522	t	2025-11-03 16:32:47.916739+02
10	Helsinki	helsinki	Finland	FI	https://picsum.photos/seed/destination-helsinki/1200/800	60.1699	24.9384	f	2025-11-03 16:32:47.916739+02
11	Reykjavik	reykjavik	Iceland	IS	https://picsum.photos/seed/destination-reykjavik/1200/800	64.1466	-21.9426	t	2025-11-03 16:32:47.916739+02
12	Bergen	bergen	Norway	NO	https://picsum.photos/seed/destination-bergen/1200/800	60.3913	5.3221	f	2025-11-03 16:32:47.916739+02
13	Paris	paris	France	FR	https://picsum.photos/seed/destination-paris/1200/800	48.8566	2.3522	t	2025-11-03 16:32:47.916739+02
14	Rome	rome	Italy	IT	https://picsum.photos/seed/destination-rome/1200/800	41.9028	12.4964	t	2025-11-03 16:32:47.916739+02
15	Tokyo	tokyo	Japan	JP	https://picsum.photos/seed/destination-tokyo/1200/800	35.6762	139.6503	t	2025-11-03 16:32:47.916739+02
18	Guangzhou	guangzhou	China	CN	https://picsum.photos/seed/destination-guangzhou/1200/800	23.1291	113.2644	t	2025-11-03 17:27:28.563347+02
19	Zhangjiajie	zhangjiajie	China	CN	https://picsum.photos/seed/destination-zhangjiajie/1200/800	29.1167	110.4792	t	2025-11-03 17:27:28.563347+02
\.


--
-- TOC entry 4205 (class 0 OID 27201)
-- Dependencies: 251
-- Data for Name: meeting_point_photos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.meeting_point_photos (id, meeting_point_id, url, caption, order_index) FROM stdin;
4	8	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-meeting-0/400/300	Meeting point view 1	0
5	8	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-meeting-1/400/300	Meeting point view 2	1
6	8	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-meeting-2/400/300	Meeting point view 3	2
7	9	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-meeting-0/400/300	Meeting point view 1	0
8	9	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-meeting-1/400/300	Meeting point view 2	1
9	9	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-meeting-2/400/300	Meeting point view 3	2
10	10	https://picsum.photos/seed/beijing-traditional-arts-temple-culture-meeting-0/400/300	Meeting point view 1	0
11	10	https://picsum.photos/seed/beijing-traditional-arts-temple-culture-meeting-1/400/300	Meeting point view 2	1
12	10	https://picsum.photos/seed/beijing-traditional-arts-temple-culture-meeting-2/400/300	Meeting point view 3	2
13	11	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-meeting-0/400/300	Meeting point view 1	0
14	11	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-meeting-1/400/300	Meeting point view 2	1
15	11	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-meeting-2/400/300	Meeting point view 3	2
16	12	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-meeting-0/400/300	Meeting point view 1	0
17	12	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-meeting-1/400/300	Meeting point view 2	1
18	12	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-meeting-2/400/300	Meeting point view 3	2
19	13	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-meeting-0/400/300	Meeting point view 1	0
20	13	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-meeting-1/400/300	Meeting point view 2	1
21	13	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-meeting-2/400/300	Meeting point view 3	2
22	14	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-meeting-0/400/300	Meeting point view 1	0
23	14	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-meeting-1/400/300	Meeting point view 2	1
24	14	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-meeting-2/400/300	Meeting point view 3	2
25	15	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-meeting-0/400/300	Meeting point view 1	0
26	15	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-meeting-1/400/300	Meeting point view 2	1
27	15	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-meeting-2/400/300	Meeting point view 3	2
28	16	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-meeting-0/400/300	Meeting point view 1	0
29	16	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-meeting-1/400/300	Meeting point view 2	1
30	16	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-meeting-2/400/300	Meeting point view 3	2
31	17	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-meeting-0/400/300	Meeting point view 1	0
32	17	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-meeting-1/400/300	Meeting point view 2	1
33	17	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-meeting-2/400/300	Meeting point view 3	2
34	18	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-meeting-0/400/300	Meeting point view 1	0
35	18	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-meeting-1/400/300	Meeting point view 2	1
36	18	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-meeting-2/400/300	Meeting point view 3	2
37	19	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-meeting-0/400/300	Meeting point view 1	0
38	19	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-meeting-1/400/300	Meeting point view 2	1
39	19	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-meeting-2/400/300	Meeting point view 3	2
40	20	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-meeting-0/400/300	Meeting point view 1	0
41	20	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-meeting-1/400/300	Meeting point view 2	1
42	20	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-meeting-2/400/300	Meeting point view 3	2
43	21	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-meeting-0/400/300	Meeting point view 1	0
44	21	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-meeting-1/400/300	Meeting point view 2	1
45	21	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-meeting-2/400/300	Meeting point view 3	2
46	22	https://picsum.photos/seed/stockholm-modern-design-architecture-walking-tour-meeting-0/400/300	Meeting point view 1	0
47	22	https://picsum.photos/seed/stockholm-modern-design-architecture-walking-tour-meeting-1/400/300	Meeting point view 2	1
48	22	https://picsum.photos/seed/stockholm-modern-design-architecture-walking-tour-meeting-2/400/300	Meeting point view 3	2
\.


--
-- TOC entry 4223 (class 0 OID 27378)
-- Dependencies: 269
-- Data for Name: meeting_point_translations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.meeting_point_translations (id, meeting_point_id, language, address, instructions, parking_info, public_transport_info, nearby_landmarks) FROM stdin;
\.


--
-- TOC entry 4188 (class 0 OID 27047)
-- Dependencies: 234
-- Data for Name: meeting_points; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.meeting_points (id, activity_id, address, instructions, latitude, longitude, parking_info, public_transport_info, nearby_landmarks) FROM stdin;
1	1	Meeting Point for Great Wall of China Private Day Tour with Lunch, Beijing	Look for guide with company sign near main entrance	39.89656874285274	116.39794819207609	Public parking available nearby	Accessible by metro and bus	Near central square and tourist information center
2	2	Meeting Point for Shanghai Food Tour: Local Street Food and Hidden Gems, Shanghai	Look for guide with company sign near main entrance	31.23297882696405	121.4786808597994	Public parking available nearby	Accessible by metro and bus	Near central square and tourist information center
3	3	Meeting Point for Stockholm University Campus & Swedish Education System Study Tour, Stockholm	Look for guide with company sign near main entrance	59.33255229866666	18.06233806139365	Public parking available nearby	Accessible by metro and bus	Near central square and tourist information center
4	4	Meeting Point for Copenhagen Design Academy & Danish Design Philosophy Workshop, Copenhagen	Look for guide with company sign near main entrance	55.66992392905984	12.561482188331402	Public parking available nearby	Accessible by metro and bus	Near central square and tourist information center
5	5	Meeting Point for Northern Lights Chase & Arctic Culture Experience, Oslo	Look for guide with company sign near main entrance	59.91369194470003	10.751810802076793	Public parking available nearby	Accessible by metro and bus	Near central square and tourist information center
6	6	Meeting Point for Xi'an Terracotta Army Discovery Tour with Ancient History, Xi'an	Look for guide with company sign near main entrance	34.336684545068444	108.9397815631866	Public parking available nearby	Accessible by metro and bus	Near central square and tourist information center
8	8	Central Meeting Point, Chengdu	Look for guide with company banner. Arrive 15 minutes early.	39.973671873629414	117.63910801498557	Street parking available nearby	Accessible by metro and bus	Near main shopping district and hotel area
9	9	Central Meeting Point, Zhangjiajie	Look for guide with company banner. Arrive 15 minutes early.	39.03933966606679	117.43835090406724	Street parking available nearby	Accessible by metro and bus	Near main shopping district and hotel area
10	10	Central Meeting Point, Beijing	Look for guide with company banner. Arrive 15 minutes early.	40.79392692615343	116.91814101197448	Street parking available nearby	Accessible by metro and bus	Near main shopping district and hotel area
11	11	Central Meeting Point, Guangzhou	Look for guide with company banner. Arrive 15 minutes early.	39.242743627491635	116.75479540836712	Street parking available nearby	Accessible by metro and bus	Near main shopping district and hotel area
12	12	Central Meeting Point, Shanghai	Look for guide with company banner. Arrive 15 minutes early.	39.439349495966795	117.04430940121539	Street parking available nearby	Accessible by metro and bus	Near main shopping district and hotel area
13	13	Central Meeting Point, Guilin	Look for guide with company banner. Arrive 15 minutes early.	40.98832491676182	116.08194921826447	Street parking available nearby	Accessible by metro and bus	Near main shopping district and hotel area
14	14	Central Meeting Point, Hangzhou	Look for guide with company banner. Arrive 15 minutes early.	39.98395918215261	116.47551370513752	Street parking available nearby	Accessible by metro and bus	Near main shopping district and hotel area
15	15	Central Meeting Point, Xian	Look for guide with company banner. Arrive 15 minutes early.	39.560054745895954	116.19385339139457	Street parking available nearby	Accessible by metro and bus	Near main shopping district and hotel area
16	16	Central Meeting Point, Oslo	Look for guide with company banner. Arrive 15 minutes early.	40.216418258649796	116.8726345904301	Street parking available nearby	Accessible by metro and bus	Near main shopping district and hotel area
17	17	Central Meeting Point, Helsinki	Look for guide with company banner. Arrive 15 minutes early.	40.9998506681291	116.83764423215477	Street parking available nearby	Accessible by metro and bus	Near main shopping district and hotel area
18	18	Central Meeting Point, Copenhagen	Look for guide with company banner. Arrive 15 minutes early.	39.710953817053856	117.6046343496383	Street parking available nearby	Accessible by metro and bus	Near main shopping district and hotel area
19	19	Central Meeting Point, Stockholm	Look for guide with company banner. Arrive 15 minutes early.	40.226440431025864	116.56013119938916	Street parking available nearby	Accessible by metro and bus	Near main shopping district and hotel area
20	20	Central Meeting Point, Bergen	Look for guide with company banner. Arrive 15 minutes early.	39.64134553917967	116.03647165023487	Street parking available nearby	Accessible by metro and bus	Near main shopping district and hotel area
21	21	Central Meeting Point, Reykjavik	Look for guide with company banner. Arrive 15 minutes early.	40.92879785082895	116.89425985689662	Street parking available nearby	Accessible by metro and bus	Near main shopping district and hotel area
22	22	Central Meeting Point, Stockholm	Look for guide with company banner. Arrive 15 minutes early.	39.22017931835617	116.27168369916801	Street parking available nearby	Accessible by metro and bus	Near main shopping district and hotel area
\.


--
-- TOC entry 4227 (class 0 OID 27410)
-- Dependencies: 273
-- Data for Name: review_categories; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.review_categories (id, review_id, category_name, rating) FROM stdin;
\.


--
-- TOC entry 4225 (class 0 OID 27395)
-- Dependencies: 271
-- Data for Name: review_images; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.review_images (id, review_id, url, caption) FROM stdin;
1	9	https://picsum.photos/seed/great-wall-private-tour-beijing-review-9-photo-1/400/300	Great photo from the tour - 1
2	12	https://picsum.photos/seed/shanghai-food-tour-street-food-review-12-photo-2/400/300	Great photo from the tour - 1
3	12	https://picsum.photos/seed/shanghai-food-tour-street-food-review-12-photo-3/400/300	Great photo from the tour - 2
4	12	https://picsum.photos/seed/shanghai-food-tour-street-food-review-12-photo-4/400/300	Great photo from the tour - 3
5	15	https://picsum.photos/seed/shanghai-food-tour-street-food-review-15-photo-5/400/300	Great photo from the tour - 1
6	16	https://picsum.photos/seed/shanghai-food-tour-street-food-review-16-photo-6/400/300	Great photo from the tour - 1
7	19	https://picsum.photos/seed/shanghai-food-tour-street-food-review-19-photo-7/400/300	Great photo from the tour - 1
8	20	https://picsum.photos/seed/shanghai-food-tour-street-food-review-20-photo-8/400/300	Great photo from the tour - 1
9	20	https://picsum.photos/seed/shanghai-food-tour-street-food-review-20-photo-9/400/300	Great photo from the tour - 2
10	20	https://picsum.photos/seed/shanghai-food-tour-street-food-review-20-photo-10/400/300	Great photo from the tour - 3
11	22	https://picsum.photos/seed/stockholm-university-study-tour-review-22-photo-11/400/300	Great photo from the tour - 1
12	23	https://picsum.photos/seed/stockholm-university-study-tour-review-23-photo-12/400/300	Great photo from the tour - 1
13	23	https://picsum.photos/seed/stockholm-university-study-tour-review-23-photo-13/400/300	Great photo from the tour - 2
14	23	https://picsum.photos/seed/stockholm-university-study-tour-review-23-photo-14/400/300	Great photo from the tour - 3
15	39	https://picsum.photos/seed/copenhagen-design-academy-workshop-review-39-photo-15/400/300	Great photo from the tour - 1
16	40	https://picsum.photos/seed/copenhagen-design-academy-workshop-review-40-photo-16/400/300	Great photo from the tour - 1
17	40	https://picsum.photos/seed/copenhagen-design-academy-workshop-review-40-photo-17/400/300	Great photo from the tour - 2
18	42	https://picsum.photos/seed/oslo-northern-lights-arctic-culture-review-42-photo-18/400/300	Great photo from the tour - 1
19	43	https://picsum.photos/seed/oslo-northern-lights-arctic-culture-review-43-photo-19/400/300	Great photo from the tour - 1
20	43	https://picsum.photos/seed/oslo-northern-lights-arctic-culture-review-43-photo-20/400/300	Great photo from the tour - 2
21	48	https://picsum.photos/seed/oslo-northern-lights-arctic-culture-review-48-photo-21/400/300	Great photo from the tour - 1
22	48	https://picsum.photos/seed/oslo-northern-lights-arctic-culture-review-48-photo-22/400/300	Great photo from the tour - 2
23	52	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-review-52-photo-23/400/300	Great photo from the tour - 1
24	53	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-review-53-photo-24/400/300	Great photo from the tour - 1
25	53	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-review-53-photo-25/400/300	Great photo from the tour - 2
26	53	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-review-53-photo-26/400/300	Great photo from the tour - 3
27	54	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-review-54-photo-27/400/300	Great photo from the tour - 1
28	54	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-review-54-photo-28/400/300	Great photo from the tour - 2
29	54	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-review-54-photo-29/400/300	Great photo from the tour - 3
30	56	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-review-56-photo-30/400/300	Great photo from the tour - 1
31	57	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-review-57-photo-31/400/300	Great photo from the tour - 1
32	57	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-review-57-photo-32/400/300	Great photo from the tour - 2
33	57	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-review-57-photo-33/400/300	Great photo from the tour - 3
34	58	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-review-58-photo-34/400/300	Great photo from the tour - 1
35	58	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-review-58-photo-35/400/300	Great photo from the tour - 2
36	58	https://picsum.photos/seed/xian-terracotta-warriors-history-tour-review-58-photo-36/400/300	Great photo from the tour - 3
37	66	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-review-66-0/400/300	Review photo 1
38	67	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-review-67-0/400/300	Review photo 1
39	68	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-review-68-0/400/300	Review photo 1
40	69	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-review-69-0/400/300	Review photo 1
41	69	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-review-69-1/400/300	Review photo 2
42	72	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-review-72-0/400/300	Review photo 1
43	73	https://picsum.photos/seed/sichuan-culinary-masterclass-chengdu-review-73-0/400/300	Review photo 1
44	74	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-review-74-0/400/300	Review photo 1
45	74	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-review-74-1/400/300	Review photo 2
46	74	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-review-74-2/400/300	Review photo 3
47	76	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-review-76-0/400/300	Review photo 1
48	76	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-review-76-1/400/300	Review photo 2
49	76	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-review-76-2/400/300	Review photo 3
50	79	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-review-79-0/400/300	Review photo 1
51	79	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-review-79-1/400/300	Review photo 2
52	84	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-review-84-0/400/300	Review photo 1
53	85	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-review-85-0/400/300	Review photo 1
54	85	https://picsum.photos/seed/zhangjiajie-avatar-mountain-photography-review-85-1/400/300	Review photo 2
55	87	https://picsum.photos/seed/beijing-traditional-arts-temple-culture-review-87-0/400/300	Review photo 1
56	92	https://picsum.photos/seed/beijing-traditional-arts-temple-culture-review-92-0/400/300	Review photo 1
57	92	https://picsum.photos/seed/beijing-traditional-arts-temple-culture-review-92-1/400/300	Review photo 2
58	92	https://picsum.photos/seed/beijing-traditional-arts-temple-culture-review-92-2/400/300	Review photo 3
59	97	https://picsum.photos/seed/beijing-traditional-arts-temple-culture-review-97-0/400/300	Review photo 1
60	99	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-review-99-0/400/300	Review photo 1
61	99	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-review-99-1/400/300	Review photo 2
62	99	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-review-99-2/400/300	Review photo 3
63	101	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-review-101-0/400/300	Review photo 1
64	102	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-review-102-0/400/300	Review photo 1
65	103	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-review-103-0/400/300	Review photo 1
66	104	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-review-104-0/400/300	Review photo 1
67	104	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-review-104-1/400/300	Review photo 2
68	105	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-review-105-0/400/300	Review photo 1
69	105	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-review-105-1/400/300	Review photo 2
70	105	https://picsum.photos/seed/guangzhou-modern-art-innovation-district-review-105-2/400/300	Review photo 3
71	112	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-review-112-0/400/300	Review photo 1
72	112	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-review-112-1/400/300	Review photo 2
73	113	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-review-113-0/400/300	Review photo 1
74	113	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-review-113-1/400/300	Review photo 2
75	116	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-review-116-0/400/300	Review photo 1
76	117	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-review-117-0/400/300	Review photo 1
77	117	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-review-117-1/400/300	Review photo 2
78	117	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-review-117-2/400/300	Review photo 3
79	118	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-review-118-0/400/300	Review photo 1
80	118	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-review-118-1/400/300	Review photo 2
81	120	https://picsum.photos/seed/shanghai-street-food-night-market-adventure-review-120-0/400/300	Review photo 1
82	122	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-review-122-0/400/300	Review photo 1
83	122	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-review-122-1/400/300	Review photo 2
84	122	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-review-122-2/400/300	Review photo 3
85	123	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-review-123-0/400/300	Review photo 1
86	123	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-review-123-1/400/300	Review photo 2
87	123	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-review-123-2/400/300	Review photo 3
88	125	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-review-125-0/400/300	Review photo 1
89	126	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-review-126-0/400/300	Review photo 1
90	128	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-review-128-0/400/300	Review photo 1
91	130	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-review-130-0/400/300	Review photo 1
92	130	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-review-130-1/400/300	Review photo 2
93	130	https://picsum.photos/seed/guilin-li-river-bamboo-rafting-countryside-review-130-2/400/300	Review photo 3
94	134	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-review-134-0/400/300	Review photo 1
95	134	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-review-134-1/400/300	Review photo 2
96	134	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-review-134-2/400/300	Review photo 3
97	135	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-review-135-0/400/300	Review photo 1
98	135	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-review-135-1/400/300	Review photo 2
99	135	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-review-135-2/400/300	Review photo 3
100	141	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-review-141-0/400/300	Review photo 1
101	141	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-review-141-1/400/300	Review photo 2
102	145	https://picsum.photos/seed/hangzhou-west-lake-cultural-heritage-walk-review-145-0/400/300	Review photo 1
103	149	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-review-149-0/400/300	Review photo 1
104	149	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-review-149-1/400/300	Review photo 2
105	150	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-review-150-0/400/300	Review photo 1
106	151	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-review-151-0/400/300	Review photo 1
107	154	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-review-154-0/400/300	Review photo 1
108	154	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-review-154-1/400/300	Review photo 2
109	155	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-review-155-0/400/300	Review photo 1
110	155	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-review-155-1/400/300	Review photo 2
111	155	https://picsum.photos/seed/xian-silk-road-history-muslim-quarter-review-155-2/400/300	Review photo 3
112	160	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-review-160-0/400/300	Review photo 1
113	160	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-review-160-1/400/300	Review photo 2
114	160	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-review-160-2/400/300	Review photo 3
115	162	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-review-162-0/400/300	Review photo 1
116	162	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-review-162-1/400/300	Review photo 2
117	162	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-review-162-2/400/300	Review photo 3
118	163	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-review-163-0/400/300	Review photo 1
119	163	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-review-163-1/400/300	Review photo 2
120	163	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-review-163-2/400/300	Review photo 3
121	164	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-review-164-0/400/300	Review photo 1
122	164	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-review-164-1/400/300	Review photo 2
123	165	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-review-165-0/400/300	Review photo 1
124	165	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-review-165-1/400/300	Review photo 2
125	168	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-review-168-0/400/300	Review photo 1
126	168	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-review-168-1/400/300	Review photo 2
127	169	https://picsum.photos/seed/university-oslo-sustainability-green-tech-study-review-169-0/400/300	Review photo 1
128	170	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-review-170-0/400/300	Review photo 1
129	171	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-review-171-0/400/300	Review photo 1
130	171	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-review-171-1/400/300	Review photo 2
131	174	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-review-174-0/400/300	Review photo 1
132	176	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-review-176-0/400/300	Review photo 1
133	180	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-review-180-0/400/300	Review photo 1
134	180	https://picsum.photos/seed/finnish-innovation-startup-ecosystem-study-review-180-1/400/300	Review photo 2
135	182	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-review-182-0/400/300	Review photo 1
136	185	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-review-185-0/400/300	Review photo 1
137	185	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-review-185-1/400/300	Review photo 2
138	185	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-review-185-2/400/300	Review photo 3
139	186	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-review-186-0/400/300	Review photo 1
140	186	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-review-186-1/400/300	Review photo 2
141	186	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-review-186-2/400/300	Review photo 3
142	188	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-review-188-0/400/300	Review photo 1
143	189	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-review-189-0/400/300	Review photo 1
144	192	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-review-192-0/400/300	Review photo 1
145	192	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-review-192-1/400/300	Review photo 2
146	192	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-review-192-2/400/300	Review photo 3
147	193	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-review-193-0/400/300	Review photo 1
148	193	https://picsum.photos/seed/danish-language-culture-immersion-copenhagen-review-193-1/400/300	Review photo 2
149	196	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-review-196-0/400/300	Review photo 1
150	196	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-review-196-1/400/300	Review photo 2
151	197	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-review-197-0/400/300	Review photo 1
152	197	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-review-197-1/400/300	Review photo 2
153	199	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-review-199-0/400/300	Review photo 1
154	199	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-review-199-1/400/300	Review photo 2
155	199	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-review-199-2/400/300	Review photo 3
156	200	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-review-200-0/400/300	Review photo 1
157	203	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-review-203-0/400/300	Review photo 1
158	203	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-review-203-1/400/300	Review photo 2
159	203	https://picsum.photos/seed/swedish-education-system-teaching-methods-study-review-203-2/400/300	Review photo 3
160	206	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-review-206-0/400/300	Review photo 1
161	209	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-review-209-0/400/300	Review photo 1
162	209	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-review-209-1/400/300	Review photo 2
163	211	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-review-211-0/400/300	Review photo 1
164	212	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-review-212-0/400/300	Review photo 1
165	215	https://picsum.photos/seed/norwegian-fjords-arctic-wildlife-photography-review-215-0/400/300	Review photo 1
166	219	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-review-219-0/400/300	Review photo 1
167	220	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-review-220-0/400/300	Review photo 1
168	220	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-review-220-1/400/300	Review photo 2
169	223	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-review-223-0/400/300	Review photo 1
170	223	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-review-223-1/400/300	Review photo 2
171	224	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-review-224-0/400/300	Review photo 1
172	224	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-review-224-1/400/300	Review photo 2
173	224	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-review-224-2/400/300	Review photo 3
174	225	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-review-225-0/400/300	Review photo 1
175	225	https://picsum.photos/seed/icelandic-geothermal-volcanic-landscape-adventure-review-225-1/400/300	Review photo 2
176	235	https://picsum.photos/seed/stockholm-modern-design-architecture-walking-tour-review-235-0/400/300	Review photo 1
177	235	https://picsum.photos/seed/stockholm-modern-design-architecture-walking-tour-review-235-1/400/300	Review photo 2
178	235	https://picsum.photos/seed/stockholm-modern-design-architecture-walking-tour-review-235-2/400/300	Review photo 3
179	238	https://picsum.photos/seed/stockholm-modern-design-architecture-walking-tour-review-238-0/400/300	Review photo 1
180	238	https://picsum.photos/seed/stockholm-modern-design-architecture-walking-tour-review-238-1/400/300	Review photo 2
\.


--
-- TOC entry 4209 (class 0 OID 27244)
-- Dependencies: 255
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.reviews (id, booking_id, user_id, activity_id, vendor_id, rating, title, comment, is_verified_booking, helpful_count, created_at, updated_at) FROM stdin;
1	\N	4	1	1	5	Unforgettable experience	This was the highlight of our trip! The guide's expertise really made the difference. We learned so much and got to see places we would never have found on our own. Excellent value for money.	t	20	2025-06-30 16:32:49.020802+03	\N
2	\N	5	1	1	4	Great tour with minor issues	Overall a fantastic experience. The main attraction was incredible and our guide was very informative. The only downside was the transportation took longer than expected, but it was still worth it.	t	8	2025-09-15 16:32:49.02247+03	\N
3	\N	8	1	1	5	Exceeded expectations	From booking to the end of the tour, everything was seamless. The guide's knowledge was impressive and they made the experience personal and engaging. Worth every penny!	t	3	2025-06-16 16:32:49.025311+03	\N
4	\N	9	1	1	4	Highly recommended	A wonderful way to experience the local culture. The guide was friendly and accommodating, and the pace was just right. The included meal was delicious. Would recommend to friends and family.	t	4	2025-05-10 16:32:49.026493+03	\N
5	\N	8	1	1	3	Decent tour but room for improvement	The tour was okay but not exceptional. The guide was nice but could have been more engaging. The pace was a bit rushed and we didn't have enough time at some locations. Not bad, but not great either.	t	25	2025-06-03 16:32:49.028026+03	\N
6	\N	5	1	1	4	Great cultural insight	Really enjoyed learning about the local history and culture. The guide shared interesting stories and answered all our questions. The tour was well-paced and informative. Would do it again!	t	8	2025-06-16 16:32:49.029274+03	\N
7	\N	3	1	1	5	Amazing experience!	This tour exceeded all my expectations. The guide was knowledgeable and friendly, and we learned so much about the local culture and history. The organization was perfect and the experience was unforgettable. Highly recommended!	t	0	2025-10-16 16:32:49.030282+03	\N
8	\N	2	1	1	4	Good experience overall	Nice tour with lots of interesting information. The guide was professional and the group was a good size. Some parts could have been longer, but overall satisfied with the experience.	t	6	2025-09-28 16:32:49.030968+03	\N
9	\N	6	1	1	5	Perfect day out	Everything was well-organized from start to finish. Our guide was passionate and shared amazing stories. The group size was perfect, not too crowded. Will definitely book again!	t	1	2025-09-17 16:32:49.031868+03	\N
10	\N	5	1	1	5	Must-do experience	This tour is a must if you're visiting the area. Our guide was fantastic - knowledgeable, funny, and really passionate about sharing the local culture. The experience was educational and fun.	t	1	2025-05-26 16:32:49.032774+03	\N
11	\N	7	2	3	5	Amazing experience!	This tour exceeded all my expectations. The guide was knowledgeable and friendly, and we learned so much about the local culture and history. The organization was perfect and the experience was unforgettable. Highly recommended!	t	17	2025-06-18 16:32:49.035934+03	\N
12	\N	7	2	3	5	Perfect day out	Everything was well-organized from start to finish. Our guide was passionate and shared amazing stories. The group size was perfect, not too crowded. Will definitely book again!	t	23	2025-08-02 16:32:49.036934+03	\N
13	\N	6	2	3	5	Exceeded expectations	From booking to the end of the tour, everything was seamless. The guide's knowledge was impressive and they made the experience personal and engaging. Worth every penny!	t	17	2025-10-16 16:32:49.03784+03	\N
14	\N	8	2	3	4	Good experience overall	Nice tour with lots of interesting information. The guide was professional and the group was a good size. Some parts could have been longer, but overall satisfied with the experience.	t	1	2025-07-25 16:32:49.039549+03	\N
15	\N	2	2	3	3	Decent tour but room for improvement	The tour was okay but not exceptional. The guide was nice but could have been more engaging. The pace was a bit rushed and we didn't have enough time at some locations. Not bad, but not great either.	t	3	2025-10-03 16:32:49.040469+03	\N
16	\N	8	2	3	5	Must-do experience	This tour is a must if you're visiting the area. Our guide was fantastic - knowledgeable, funny, and really passionate about sharing the local culture. The experience was educational and fun.	t	5	2025-10-04 16:32:49.041366+03	\N
17	\N	5	2	3	4	Great cultural insight	Really enjoyed learning about the local history and culture. The guide shared interesting stories and answered all our questions. The tour was well-paced and informative. Would do it again!	t	16	2025-10-14 16:32:49.042586+03	\N
18	\N	7	2	3	4	Great tour with minor issues	Overall a fantastic experience. The main attraction was incredible and our guide was very informative. The only downside was the transportation took longer than expected, but it was still worth it.	t	15	2025-07-17 16:32:49.043939+03	\N
19	\N	5	2	3	4	Highly recommended	A wonderful way to experience the local culture. The guide was friendly and accommodating, and the pace was just right. The included meal was delicious. Would recommend to friends and family.	t	5	2025-05-11 16:32:49.044873+03	\N
20	\N	6	2	3	5	Unforgettable experience	This was the highlight of our trip! The guide's expertise really made the difference. We learned so much and got to see places we would never have found on our own. Excellent value for money.	t	17	2025-06-05 16:32:49.045928+03	\N
21	\N	9	3	2	4	Great cultural insight	Really enjoyed learning about the local history and culture. The guide shared interesting stories and answered all our questions. The tour was well-paced and informative. Would do it again!	t	23	2025-05-27 16:32:49.047124+03	\N
22	\N	2	3	2	4	Great tour with minor issues	Overall a fantastic experience. The main attraction was incredible and our guide was very informative. The only downside was the transportation took longer than expected, but it was still worth it.	t	7	2025-09-24 16:32:49.048478+03	\N
23	\N	8	3	2	5	Must-do experience	This tour is a must if you're visiting the area. Our guide was fantastic - knowledgeable, funny, and really passionate about sharing the local culture. The experience was educational and fun.	t	0	2025-10-12 16:32:49.049379+03	\N
24	\N	2	3	2	5	Unforgettable experience	This was the highlight of our trip! The guide's expertise really made the difference. We learned so much and got to see places we would never have found on our own. Excellent value for money.	t	23	2025-05-17 16:32:49.050552+03	\N
25	\N	2	3	2	4	Highly recommended	A wonderful way to experience the local culture. The guide was friendly and accommodating, and the pace was just right. The included meal was delicious. Would recommend to friends and family.	t	10	2025-07-30 16:32:49.051939+03	\N
26	\N	6	3	2	5	Perfect day out	Everything was well-organized from start to finish. Our guide was passionate and shared amazing stories. The group size was perfect, not too crowded. Will definitely book again!	t	5	2025-09-11 16:32:49.053374+03	\N
27	\N	4	3	2	3	Decent tour but room for improvement	The tour was okay but not exceptional. The guide was nice but could have been more engaging. The pace was a bit rushed and we didn't have enough time at some locations. Not bad, but not great either.	t	16	2025-05-22 16:32:49.05439+03	\N
28	\N	3	3	2	4	Good experience overall	Nice tour with lots of interesting information. The guide was professional and the group was a good size. Some parts could have been longer, but overall satisfied with the experience.	t	8	2025-05-25 16:32:49.05536+03	\N
29	\N	3	3	2	5	Amazing experience!	This tour exceeded all my expectations. The guide was knowledgeable and friendly, and we learned so much about the local culture and history. The organization was perfect and the experience was unforgettable. Highly recommended!	t	19	2025-07-10 16:32:49.056271+03	\N
30	\N	4	3	2	5	Exceeded expectations	From booking to the end of the tour, everything was seamless. The guide's knowledge was impressive and they made the experience personal and engaging. Worth every penny!	t	14	2025-07-31 16:32:49.058224+03	\N
31	\N	9	4	4	5	Unforgettable experience	This was the highlight of our trip! The guide's expertise really made the difference. We learned so much and got to see places we would never have found on our own. Excellent value for money.	t	22	2025-08-10 16:32:49.059202+03	\N
32	\N	5	4	4	5	Perfect day out	Everything was well-organized from start to finish. Our guide was passionate and shared amazing stories. The group size was perfect, not too crowded. Will definitely book again!	t	22	2025-06-14 16:32:49.060126+03	\N
33	\N	7	4	4	4	Great cultural insight	Really enjoyed learning about the local history and culture. The guide shared interesting stories and answered all our questions. The tour was well-paced and informative. Would do it again!	t	2	2025-10-20 16:32:49.061125+03	\N
34	\N	5	4	4	4	Highly recommended	A wonderful way to experience the local culture. The guide was friendly and accommodating, and the pace was just right. The included meal was delicious. Would recommend to friends and family.	t	17	2025-11-01 16:32:49.062179+02	\N
35	\N	6	4	4	5	Exceeded expectations	From booking to the end of the tour, everything was seamless. The guide's knowledge was impressive and they made the experience personal and engaging. Worth every penny!	t	0	2025-07-17 16:32:49.06319+03	\N
36	\N	6	4	4	3	Decent tour but room for improvement	The tour was okay but not exceptional. The guide was nice but could have been more engaging. The pace was a bit rushed and we didn't have enough time at some locations. Not bad, but not great either.	t	11	2025-06-20 16:32:49.064171+03	\N
37	\N	9	4	4	4	Great tour with minor issues	Overall a fantastic experience. The main attraction was incredible and our guide was very informative. The only downside was the transportation took longer than expected, but it was still worth it.	t	8	2025-09-17 16:32:49.065121+03	\N
38	\N	9	4	4	5	Amazing experience!	This tour exceeded all my expectations. The guide was knowledgeable and friendly, and we learned so much about the local culture and history. The organization was perfect and the experience was unforgettable. Highly recommended!	t	24	2025-08-07 16:32:49.066077+03	\N
39	\N	6	4	4	4	Good experience overall	Nice tour with lots of interesting information. The guide was professional and the group was a good size. Some parts could have been longer, but overall satisfied with the experience.	t	6	2025-06-13 16:32:49.067022+03	\N
40	\N	6	4	4	5	Must-do experience	This tour is a must if you're visiting the area. Our guide was fantastic - knowledgeable, funny, and really passionate about sharing the local culture. The experience was educational and fun.	t	6	2025-05-14 16:32:49.06799+03	\N
41	\N	5	5	6	5	Amazing experience!	This tour exceeded all my expectations. The guide was knowledgeable and friendly, and we learned so much about the local culture and history. The organization was perfect and the experience was unforgettable. Highly recommended!	t	25	2025-05-10 16:32:49.070112+03	\N
42	\N	6	5	6	4	Good experience overall	Nice tour with lots of interesting information. The guide was professional and the group was a good size. Some parts could have been longer, but overall satisfied with the experience.	t	25	2025-05-13 16:32:49.071668+03	\N
43	\N	3	5	6	5	Unforgettable experience	This was the highlight of our trip! The guide's expertise really made the difference. We learned so much and got to see places we would never have found on our own. Excellent value for money.	t	13	2025-07-15 16:32:49.072803+03	\N
44	\N	2	5	6	5	Perfect day out	Everything was well-organized from start to finish. Our guide was passionate and shared amazing stories. The group size was perfect, not too crowded. Will definitely book again!	t	5	2025-07-03 16:32:49.074159+03	\N
45	\N	7	5	6	5	Must-do experience	This tour is a must if you're visiting the area. Our guide was fantastic - knowledgeable, funny, and really passionate about sharing the local culture. The experience was educational and fun.	t	1	2025-09-02 16:32:49.075675+03	\N
46	\N	7	5	6	4	Highly recommended	A wonderful way to experience the local culture. The guide was friendly and accommodating, and the pace was just right. The included meal was delicious. Would recommend to friends and family.	t	14	2025-08-22 16:32:49.076682+03	\N
47	\N	6	5	6	4	Great cultural insight	Really enjoyed learning about the local history and culture. The guide shared interesting stories and answered all our questions. The tour was well-paced and informative. Would do it again!	t	18	2025-05-09 16:32:49.077662+03	\N
48	\N	3	5	6	3	Decent tour but room for improvement	The tour was okay but not exceptional. The guide was nice but could have been more engaging. The pace was a bit rushed and we didn't have enough time at some locations. Not bad, but not great either.	t	7	2025-07-15 16:32:49.079459+03	\N
49	\N	2	5	6	4	Great tour with minor issues	Overall a fantastic experience. The main attraction was incredible and our guide was very informative. The only downside was the transportation took longer than expected, but it was still worth it.	t	3	2025-07-21 16:32:49.080471+03	\N
50	\N	4	5	6	5	Exceeded expectations	From booking to the end of the tour, everything was seamless. The guide's knowledge was impressive and they made the experience personal and engaging. Worth every penny!	t	10	2025-07-15 16:32:49.081986+03	\N
51	\N	7	6	5	5	Unforgettable experience	This was the highlight of our trip! The guide's expertise really made the difference. We learned so much and got to see places we would never have found on our own. Excellent value for money.	t	19	2025-07-11 16:32:49.083064+03	\N
52	\N	6	6	5	5	Must-do experience	This tour is a must if you're visiting the area. Our guide was fantastic - knowledgeable, funny, and really passionate about sharing the local culture. The experience was educational and fun.	t	24	2025-07-06 16:32:49.084058+03	\N
53	\N	7	6	5	5	Perfect day out	Everything was well-organized from start to finish. Our guide was passionate and shared amazing stories. The group size was perfect, not too crowded. Will definitely book again!	t	22	2025-06-01 16:32:49.085237+03	\N
54	\N	8	6	5	4	Great cultural insight	Really enjoyed learning about the local history and culture. The guide shared interesting stories and answered all our questions. The tour was well-paced and informative. Would do it again!	t	12	2025-06-26 16:32:49.086547+03	\N
55	\N	9	6	5	4	Great tour with minor issues	Overall a fantastic experience. The main attraction was incredible and our guide was very informative. The only downside was the transportation took longer than expected, but it was still worth it.	t	3	2025-09-06 16:32:49.088044+03	\N
56	\N	7	6	5	4	Highly recommended	A wonderful way to experience the local culture. The guide was friendly and accommodating, and the pace was just right. The included meal was delicious. Would recommend to friends and family.	t	14	2025-07-04 16:32:49.089489+03	\N
57	\N	3	6	5	5	Exceeded expectations	From booking to the end of the tour, everything was seamless. The guide's knowledge was impressive and they made the experience personal and engaging. Worth every penny!	t	7	2025-06-27 16:32:49.090393+03	\N
58	\N	2	6	5	4	Good experience overall	Nice tour with lots of interesting information. The guide was professional and the group was a good size. Some parts could have been longer, but overall satisfied with the experience.	t	9	2025-10-22 16:32:49.091659+03	\N
59	\N	6	6	5	3	Decent tour but room for improvement	The tour was okay but not exceptional. The guide was nice but could have been more engaging. The pace was a bit rushed and we didn't have enough time at some locations. Not bad, but not great either.	t	14	2025-08-09 16:32:49.093206+03	\N
60	\N	8	6	5	5	Amazing experience!	This tour exceeded all my expectations. The guide was knowledgeable and friendly, and we learned so much about the local culture and history. The organization was perfect and the experience was unforgettable. Highly recommended!	t	12	2025-09-13 16:32:49.094768+03	\N
62	\N	2	8	8	5	Amazing experience!	Absolutely loved this tour. The guide was knowledgeable and the experience was unforgettable.	f	1	2025-10-09 17:27:28.755851+03	\N
63	\N	3	8	8	5	Highly recommended	Perfect organization, great value for money. Would definitely do this again.	t	13	2025-08-21 17:27:28.760752+03	\N
64	\N	4	8	8	4	Great tour	Really enjoyed the experience. Minor delays but overall fantastic.	t	11	2025-08-23 17:27:28.761297+03	\N
65	\N	5	8	8	5	Exceeded expectations	This tour was even better than described. Authentic and well-organized.	f	5	2025-10-24 17:27:28.761798+03	\N
66	\N	6	8	8	4	Very good	Good experience with professional guide. Worth the price.	t	7	2025-10-22 17:27:28.762105+03	\N
67	\N	7	8	8	5	Outstanding	One of the best tours I've ever taken. Highly professional and informative.	f	11	2025-10-06 17:27:28.762465+03	\N
68	\N	8	8	8	4	Enjoyed it	Nice experience, learned a lot. Would recommend to friends.	t	14	2025-08-28 17:27:28.763769+03	\N
69	\N	9	8	8	5	Perfect!	Everything was perfect from start to finish. Amazing attention to detail.	f	4	2025-09-21 17:27:28.764496+03	\N
70	\N	18	8	8	4	Good value	Fair price for what you get. Guide was very friendly and helpful.	f	3	2025-08-22 17:27:28.931855+03	\N
71	\N	19	8	8	5	Memorable	Created lasting memories. The whole family enjoyed every moment.	f	9	2025-09-24 17:27:29.097795+03	\N
72	\N	20	8	8	4	Well organized	Professional service, on time, and well planned. Minor room for improvement.	t	2	2025-09-19 17:27:29.262956+03	\N
73	\N	21	8	8	5	Fantastic!	Couldn't have asked for a better experience. Will book again next visit.	t	12	2025-08-22 17:27:29.42918+03	\N
74	\N	2	9	8	5	Amazing experience!	Absolutely loved this tour. The guide was knowledgeable and the experience was unforgettable.	f	10	2025-10-11 17:27:29.438894+03	\N
75	\N	3	9	8	5	Highly recommended	Perfect organization, great value for money. Would definitely do this again.	t	5	2025-08-08 17:27:29.440452+03	\N
76	\N	4	9	8	4	Great tour	Really enjoyed the experience. Minor delays but overall fantastic.	f	14	2025-10-14 17:27:29.441355+03	\N
77	\N	5	9	8	5	Exceeded expectations	This tour was even better than described. Authentic and well-organized.	t	10	2025-09-27 17:27:29.441752+03	\N
78	\N	6	9	8	4	Very good	Good experience with professional guide. Worth the price.	t	13	2025-09-22 17:27:29.442626+03	\N
79	\N	7	9	8	5	Outstanding	One of the best tours I've ever taken. Highly professional and informative.	t	14	2025-09-09 17:27:29.442987+03	\N
80	\N	8	9	8	4	Enjoyed it	Nice experience, learned a lot. Would recommend to friends.	t	2	2025-09-26 17:27:29.443353+03	\N
81	\N	9	9	8	5	Perfect!	Everything was perfect from start to finish. Amazing attention to detail.	t	6	2025-10-18 17:27:29.444113+03	\N
82	\N	18	9	8	4	Good value	Fair price for what you get. Guide was very friendly and helpful.	f	14	2025-10-15 17:27:29.444502+03	\N
83	\N	19	9	8	5	Memorable	Created lasting memories. The whole family enjoyed every moment.	t	12	2025-10-10 17:27:29.444842+03	\N
84	\N	20	9	8	4	Well organized	Professional service, on time, and well planned. Minor room for improvement.	f	7	2025-08-21 17:27:29.445172+03	\N
85	\N	21	9	8	5	Fantastic!	Couldn't have asked for a better experience. Will book again next visit.	t	14	2025-09-14 17:27:29.44565+03	\N
86	\N	2	10	8	5	Amazing experience!	Absolutely loved this tour. The guide was knowledgeable and the experience was unforgettable.	t	2	2025-08-10 17:27:29.451661+03	\N
87	\N	3	10	8	5	Highly recommended	Perfect organization, great value for money. Would definitely do this again.	f	9	2025-09-04 17:27:29.452357+03	\N
88	\N	4	10	8	4	Great tour	Really enjoyed the experience. Minor delays but overall fantastic.	f	11	2025-10-16 17:27:29.452678+03	\N
89	\N	5	10	8	5	Exceeded expectations	This tour was even better than described. Authentic and well-organized.	f	9	2025-11-01 17:27:29.453209+02	\N
90	\N	6	10	8	4	Very good	Good experience with professional guide. Worth the price.	t	2	2025-08-13 17:27:29.453506+03	\N
91	\N	7	10	8	5	Outstanding	One of the best tours I've ever taken. Highly professional and informative.	f	15	2025-09-08 17:27:29.453818+03	\N
92	\N	8	10	8	4	Enjoyed it	Nice experience, learned a lot. Would recommend to friends.	t	4	2025-10-02 17:27:29.454156+03	\N
93	\N	9	10	8	5	Perfect!	Everything was perfect from start to finish. Amazing attention to detail.	t	4	2025-08-06 17:27:29.454497+03	\N
94	\N	18	10	8	4	Good value	Fair price for what you get. Guide was very friendly and helpful.	f	13	2025-10-03 17:27:29.455203+03	\N
95	\N	19	10	8	5	Memorable	Created lasting memories. The whole family enjoyed every moment.	f	11	2025-09-25 17:27:29.455507+03	\N
96	\N	20	10	8	4	Well organized	Professional service, on time, and well planned. Minor room for improvement.	t	1	2025-08-24 17:27:29.456017+03	\N
97	\N	21	10	8	5	Fantastic!	Couldn't have asked for a better experience. Will book again next visit.	f	0	2025-11-01 17:27:29.456339+02	\N
98	\N	2	11	8	5	Amazing experience!	Absolutely loved this tour. The guide was knowledgeable and the experience was unforgettable.	t	14	2025-09-29 17:27:29.461083+03	\N
99	\N	3	11	8	5	Highly recommended	Perfect organization, great value for money. Would definitely do this again.	f	11	2025-10-10 17:27:29.461705+03	\N
100	\N	4	11	8	4	Great tour	Really enjoyed the experience. Minor delays but overall fantastic.	f	11	2025-09-14 17:27:29.462009+03	\N
101	\N	5	11	8	5	Exceeded expectations	This tour was even better than described. Authentic and well-organized.	f	11	2025-09-24 17:27:29.462708+03	\N
102	\N	6	11	8	4	Very good	Good experience with professional guide. Worth the price.	f	10	2025-10-31 17:27:29.463001+02	\N
103	\N	7	11	8	5	Outstanding	One of the best tours I've ever taken. Highly professional and informative.	f	14	2025-09-26 17:27:29.463486+03	\N
104	\N	8	11	8	4	Enjoyed it	Nice experience, learned a lot. Would recommend to friends.	t	3	2025-09-20 17:27:29.464062+03	\N
105	\N	9	11	8	5	Perfect!	Everything was perfect from start to finish. Amazing attention to detail.	f	8	2025-09-26 17:27:29.464523+03	\N
106	\N	18	11	8	4	Good value	Fair price for what you get. Guide was very friendly and helpful.	t	9	2025-08-16 17:27:29.465123+03	\N
107	\N	19	11	8	5	Memorable	Created lasting memories. The whole family enjoyed every moment.	f	7	2025-09-04 17:27:29.46635+03	\N
108	\N	20	11	8	4	Well organized	Professional service, on time, and well planned. Minor room for improvement.	t	13	2025-09-21 17:27:29.466611+03	\N
109	\N	21	11	8	5	Fantastic!	Couldn't have asked for a better experience. Will book again next visit.	t	3	2025-08-24 17:27:29.466865+03	\N
110	\N	2	12	8	5	Amazing experience!	Absolutely loved this tour. The guide was knowledgeable and the experience was unforgettable.	t	2	2025-10-19 17:27:29.470163+03	\N
111	\N	3	12	8	5	Highly recommended	Perfect organization, great value for money. Would definitely do this again.	f	12	2025-10-28 17:27:29.470711+02	\N
112	\N	4	12	8	4	Great tour	Really enjoyed the experience. Minor delays but overall fantastic.	t	9	2025-08-28 17:27:29.470971+03	\N
113	\N	5	12	8	5	Exceeded expectations	This tour was even better than described. Authentic and well-organized.	t	4	2025-09-14 17:27:29.471266+03	\N
114	\N	6	12	8	4	Very good	Good experience with professional guide. Worth the price.	t	8	2025-09-27 17:27:29.471934+03	\N
115	\N	7	12	8	5	Outstanding	One of the best tours I've ever taken. Highly professional and informative.	t	8	2025-08-19 17:27:29.472484+03	\N
116	\N	8	12	8	4	Enjoyed it	Nice experience, learned a lot. Would recommend to friends.	f	7	2025-08-13 17:27:29.472735+03	\N
117	\N	9	12	8	5	Perfect!	Everything was perfect from start to finish. Amazing attention to detail.	t	0	2025-10-23 17:27:29.472995+03	\N
118	\N	18	12	8	4	Good value	Fair price for what you get. Guide was very friendly and helpful.	f	10	2025-08-14 17:27:29.473447+03	\N
119	\N	19	12	8	5	Memorable	Created lasting memories. The whole family enjoyed every moment.	f	13	2025-08-05 17:27:29.47402+03	\N
120	\N	20	12	8	4	Well organized	Professional service, on time, and well planned. Minor room for improvement.	t	3	2025-08-30 17:27:29.474824+03	\N
121	\N	21	12	8	5	Fantastic!	Couldn't have asked for a better experience. Will book again next visit.	t	13	2025-09-27 17:27:29.475103+03	\N
122	\N	2	13	8	5	Amazing experience!	Absolutely loved this tour. The guide was knowledgeable and the experience was unforgettable.	f	7	2025-09-04 17:27:29.482148+03	\N
123	\N	3	13	8	5	Highly recommended	Perfect organization, great value for money. Would definitely do this again.	f	9	2025-10-30 17:27:29.48284+02	\N
124	\N	4	13	8	4	Great tour	Really enjoyed the experience. Minor delays but overall fantastic.	f	5	2025-10-29 17:27:29.4835+02	\N
125	\N	5	13	8	5	Exceeded expectations	This tour was even better than described. Authentic and well-organized.	t	7	2025-08-05 17:27:29.484086+03	\N
126	\N	6	13	8	4	Very good	Good experience with professional guide. Worth the price.	f	0	2025-08-30 17:27:29.484363+03	\N
127	\N	7	13	8	5	Outstanding	One of the best tours I've ever taken. Highly professional and informative.	f	10	2025-09-09 17:27:29.484819+03	\N
128	\N	8	13	8	4	Enjoyed it	Nice experience, learned a lot. Would recommend to friends.	f	0	2025-08-21 17:27:29.48525+03	\N
129	\N	9	13	8	5	Perfect!	Everything was perfect from start to finish. Amazing attention to detail.	t	0	2025-09-04 17:27:29.485512+03	\N
130	\N	18	13	8	4	Good value	Fair price for what you get. Guide was very friendly and helpful.	t	1	2025-10-19 17:27:29.485945+03	\N
131	\N	19	13	8	5	Memorable	Created lasting memories. The whole family enjoyed every moment.	f	2	2025-09-27 17:27:29.48622+03	\N
132	\N	20	13	8	4	Well organized	Professional service, on time, and well planned. Minor room for improvement.	t	12	2025-09-11 17:27:29.486773+03	\N
133	\N	21	13	8	5	Fantastic!	Couldn't have asked for a better experience. Will book again next visit.	t	4	2025-08-29 17:27:29.487019+03	\N
134	\N	2	14	8	5	Amazing experience!	Absolutely loved this tour. The guide was knowledgeable and the experience was unforgettable.	t	10	2025-09-21 17:27:29.490344+03	\N
135	\N	3	14	8	5	Highly recommended	Perfect organization, great value for money. Would definitely do this again.	t	2	2025-08-26 17:27:29.490917+03	\N
136	\N	4	14	8	4	Great tour	Really enjoyed the experience. Minor delays but overall fantastic.	f	2	2025-08-15 17:27:29.491519+03	\N
137	\N	5	14	8	5	Exceeded expectations	This tour was even better than described. Authentic and well-organized.	f	8	2025-08-22 17:27:29.492076+03	\N
138	\N	6	14	8	4	Very good	Good experience with professional guide. Worth the price.	t	13	2025-08-15 17:27:29.492329+03	\N
139	\N	7	14	8	5	Outstanding	One of the best tours I've ever taken. Highly professional and informative.	f	1	2025-10-19 17:27:29.492582+03	\N
140	\N	8	14	8	4	Enjoyed it	Nice experience, learned a lot. Would recommend to friends.	t	2	2025-08-08 17:27:29.492823+03	\N
141	\N	9	14	8	5	Perfect!	Everything was perfect from start to finish. Amazing attention to detail.	f	3	2025-08-26 17:27:29.493075+03	\N
142	\N	18	14	8	4	Good value	Fair price for what you get. Guide was very friendly and helpful.	t	13	2025-08-19 17:27:29.493334+03	\N
143	\N	19	14	8	5	Memorable	Created lasting memories. The whole family enjoyed every moment.	t	3	2025-10-07 17:27:29.493862+03	\N
144	\N	20	14	8	4	Well organized	Professional service, on time, and well planned. Minor room for improvement.	t	0	2025-08-06 17:27:29.494111+03	\N
145	\N	21	14	8	5	Fantastic!	Couldn't have asked for a better experience. Will book again next visit.	t	11	2025-10-05 17:27:29.494358+03	\N
146	\N	2	15	8	5	Amazing experience!	Absolutely loved this tour. The guide was knowledgeable and the experience was unforgettable.	f	5	2025-10-06 17:27:29.497926+03	\N
147	\N	3	15	8	5	Highly recommended	Perfect organization, great value for money. Would definitely do this again.	t	7	2025-11-01 17:27:29.498472+02	\N
148	\N	4	15	8	4	Great tour	Really enjoyed the experience. Minor delays but overall fantastic.	t	8	2025-09-25 17:27:29.498721+03	\N
149	\N	5	15	8	5	Exceeded expectations	This tour was even better than described. Authentic and well-organized.	f	10	2025-09-19 17:27:29.498987+03	\N
150	\N	6	15	8	4	Very good	Good experience with professional guide. Worth the price.	t	0	2025-10-14 17:27:29.499274+03	\N
151	\N	7	15	8	5	Outstanding	One of the best tours I've ever taken. Highly professional and informative.	f	15	2025-10-23 17:27:29.499837+03	\N
152	\N	8	15	8	4	Enjoyed it	Nice experience, learned a lot. Would recommend to friends.	f	8	2025-10-25 17:27:29.500297+03	\N
153	\N	9	15	8	5	Perfect!	Everything was perfect from start to finish. Amazing attention to detail.	t	8	2025-09-14 17:27:29.500738+03	\N
154	\N	18	15	8	4	Good value	Fair price for what you get. Guide was very friendly and helpful.	t	12	2025-09-22 17:27:29.500992+03	\N
155	\N	19	15	8	5	Memorable	Created lasting memories. The whole family enjoyed every moment.	t	1	2025-08-15 17:27:29.501294+03	\N
156	\N	20	15	8	4	Well organized	Professional service, on time, and well planned. Minor room for improvement.	t	2	2025-10-20 17:27:29.501856+03	\N
157	\N	21	15	8	5	Fantastic!	Couldn't have asked for a better experience. Will book again next visit.	t	12	2025-10-31 17:27:29.502421+02	\N
158	\N	2	16	8	5	Amazing experience!	Absolutely loved this tour. The guide was knowledgeable and the experience was unforgettable.	t	15	2025-09-28 17:27:29.505895+03	\N
159	\N	3	16	8	5	Highly recommended	Perfect organization, great value for money. Would definitely do this again.	t	1	2025-10-30 17:27:29.506552+02	\N
160	\N	4	16	8	4	Great tour	Really enjoyed the experience. Minor delays but overall fantastic.	f	11	2025-10-20 17:27:29.506821+03	\N
161	\N	5	16	8	5	Exceeded expectations	This tour was even better than described. Authentic and well-organized.	t	2	2025-08-29 17:27:29.507126+03	\N
162	\N	6	16	8	4	Very good	Good experience with professional guide. Worth the price.	f	4	2025-08-14 17:27:29.507836+03	\N
163	\N	7	16	8	5	Outstanding	One of the best tours I've ever taken. Highly professional and informative.	f	8	2025-10-26 17:27:29.508128+02	\N
164	\N	8	16	8	4	Enjoyed it	Nice experience, learned a lot. Would recommend to friends.	f	10	2025-09-19 17:27:29.508721+03	\N
165	\N	9	16	8	5	Perfect!	Everything was perfect from start to finish. Amazing attention to detail.	t	7	2025-09-24 17:27:29.509445+03	\N
166	\N	18	16	8	4	Good value	Fair price for what you get. Guide was very friendly and helpful.	t	9	2025-09-11 17:27:29.509999+03	\N
167	\N	19	16	8	5	Memorable	Created lasting memories. The whole family enjoyed every moment.	t	14	2025-09-08 17:27:29.510615+03	\N
168	\N	20	16	8	4	Well organized	Professional service, on time, and well planned. Minor room for improvement.	t	4	2025-08-12 17:27:29.510871+03	\N
169	\N	21	16	8	5	Fantastic!	Couldn't have asked for a better experience. Will book again next visit.	t	13	2025-09-18 17:27:29.511135+03	\N
170	\N	2	17	8	5	Amazing experience!	Absolutely loved this tour. The guide was knowledgeable and the experience was unforgettable.	f	13	2025-08-26 17:27:29.517216+03	\N
171	\N	3	17	8	5	Highly recommended	Perfect organization, great value for money. Would definitely do this again.	f	14	2025-10-04 17:27:29.517838+03	\N
172	\N	4	17	8	4	Great tour	Really enjoyed the experience. Minor delays but overall fantastic.	f	4	2025-09-29 17:27:29.518314+03	\N
173	\N	5	17	8	5	Exceeded expectations	This tour was even better than described. Authentic and well-organized.	t	10	2025-10-16 17:27:29.518988+03	\N
174	\N	6	17	8	4	Very good	Good experience with professional guide. Worth the price.	f	0	2025-10-02 17:27:29.51925+03	\N
175	\N	7	17	8	5	Outstanding	One of the best tours I've ever taken. Highly professional and informative.	f	10	2025-10-15 17:27:29.519501+03	\N
176	\N	8	17	8	4	Enjoyed it	Nice experience, learned a lot. Would recommend to friends.	t	10	2025-10-22 17:27:29.519929+03	\N
177	\N	9	17	8	5	Perfect!	Everything was perfect from start to finish. Amazing attention to detail.	f	14	2025-10-22 17:27:29.520177+03	\N
178	\N	18	17	8	4	Good value	Fair price for what you get. Guide was very friendly and helpful.	f	14	2025-08-30 17:27:29.52063+03	\N
179	\N	19	17	8	5	Memorable	Created lasting memories. The whole family enjoyed every moment.	t	7	2025-08-21 17:27:29.521179+03	\N
180	\N	20	17	8	4	Well organized	Professional service, on time, and well planned. Minor room for improvement.	f	3	2025-09-24 17:27:29.52159+03	\N
181	\N	21	17	8	5	Fantastic!	Couldn't have asked for a better experience. Will book again next visit.	f	9	2025-10-30 17:27:29.523194+02	\N
182	\N	2	18	8	5	Amazing experience!	Absolutely loved this tour. The guide was knowledgeable and the experience was unforgettable.	f	10	2025-08-13 17:27:29.529497+03	\N
183	\N	3	18	8	5	Highly recommended	Perfect organization, great value for money. Would definitely do this again.	t	10	2025-10-26 17:27:29.530069+02	\N
184	\N	4	18	8	4	Great tour	Really enjoyed the experience. Minor delays but overall fantastic.	t	6	2025-09-19 17:27:29.530673+03	\N
185	\N	5	18	8	5	Exceeded expectations	This tour was even better than described. Authentic and well-organized.	f	14	2025-08-21 17:27:29.530966+03	\N
186	\N	6	18	8	4	Very good	Good experience with professional guide. Worth the price.	t	10	2025-09-26 17:27:29.531219+03	\N
187	\N	7	18	8	5	Outstanding	One of the best tours I've ever taken. Highly professional and informative.	f	14	2025-10-05 17:27:29.531784+03	\N
188	\N	8	18	8	4	Enjoyed it	Nice experience, learned a lot. Would recommend to friends.	f	0	2025-10-03 17:27:29.532369+03	\N
189	\N	9	18	8	5	Perfect!	Everything was perfect from start to finish. Amazing attention to detail.	f	4	2025-08-18 17:27:29.53262+03	\N
190	\N	18	18	8	4	Good value	Fair price for what you get. Guide was very friendly and helpful.	f	8	2025-09-22 17:27:29.533032+03	\N
191	\N	19	18	8	5	Memorable	Created lasting memories. The whole family enjoyed every moment.	t	10	2025-10-03 17:27:29.533418+03	\N
192	\N	20	18	8	4	Well organized	Professional service, on time, and well planned. Minor room for improvement.	t	2	2025-09-16 17:27:29.533634+03	\N
193	\N	21	18	8	5	Fantastic!	Couldn't have asked for a better experience. Will book again next visit.	f	2	2025-10-03 17:27:29.533874+03	\N
194	\N	2	19	8	5	Amazing experience!	Absolutely loved this tour. The guide was knowledgeable and the experience was unforgettable.	t	12	2025-08-08 17:27:29.537898+03	\N
195	\N	3	19	8	5	Highly recommended	Perfect organization, great value for money. Would definitely do this again.	t	1	2025-10-21 17:27:29.538619+03	\N
196	\N	4	19	8	4	Great tour	Really enjoyed the experience. Minor delays but overall fantastic.	t	15	2025-10-31 17:27:29.538863+02	\N
197	\N	5	19	8	5	Exceeded expectations	This tour was even better than described. Authentic and well-organized.	t	15	2025-11-02 17:27:29.539151+02	\N
198	\N	6	19	8	4	Very good	Good experience with professional guide. Worth the price.	t	7	2025-09-17 17:27:29.539847+03	\N
199	\N	7	19	8	5	Outstanding	One of the best tours I've ever taken. Highly professional and informative.	f	2	2025-10-19 17:27:29.54039+03	\N
200	\N	8	19	8	4	Enjoyed it	Nice experience, learned a lot. Would recommend to friends.	f	7	2025-08-31 17:27:29.540645+03	\N
201	\N	9	19	8	5	Perfect!	Everything was perfect from start to finish. Amazing attention to detail.	t	13	2025-10-09 17:27:29.541175+03	\N
202	\N	18	19	8	4	Good value	Fair price for what you get. Guide was very friendly and helpful.	t	6	2025-08-16 17:27:29.541571+03	\N
203	\N	19	19	8	5	Memorable	Created lasting memories. The whole family enjoyed every moment.	t	14	2025-09-10 17:27:29.541792+03	\N
204	\N	20	19	8	4	Well organized	Professional service, on time, and well planned. Minor room for improvement.	t	7	2025-10-06 17:27:29.542035+03	\N
205	\N	21	19	8	5	Fantastic!	Couldn't have asked for a better experience. Will book again next visit.	t	8	2025-09-15 17:27:29.542558+03	\N
206	\N	2	20	8	5	Amazing experience!	Absolutely loved this tour. The guide was knowledgeable and the experience was unforgettable.	t	0	2025-08-29 17:27:29.545681+03	\N
207	\N	3	20	8	5	Highly recommended	Perfect organization, great value for money. Would definitely do this again.	t	8	2025-10-22 17:27:29.546274+03	\N
208	\N	4	20	8	4	Great tour	Really enjoyed the experience. Minor delays but overall fantastic.	t	15	2025-09-21 17:27:29.547075+03	\N
209	\N	5	20	8	5	Exceeded expectations	This tour was even better than described. Authentic and well-organized.	f	1	2025-08-29 17:27:29.54737+03	\N
210	\N	6	20	8	4	Very good	Good experience with professional guide. Worth the price.	f	9	2025-08-27 17:27:29.547759+03	\N
211	\N	7	20	8	5	Outstanding	One of the best tours I've ever taken. Highly professional and informative.	t	6	2025-10-15 17:27:29.548429+03	\N
212	\N	8	20	8	4	Enjoyed it	Nice experience, learned a lot. Would recommend to friends.	f	0	2025-09-22 17:27:29.548704+03	\N
213	\N	9	20	8	5	Perfect!	Everything was perfect from start to finish. Amazing attention to detail.	f	2	2025-09-20 17:27:29.549109+03	\N
214	\N	18	20	8	4	Good value	Fair price for what you get. Guide was very friendly and helpful.	t	3	2025-09-21 17:27:29.549488+03	\N
215	\N	19	20	8	5	Memorable	Created lasting memories. The whole family enjoyed every moment.	t	5	2025-10-18 17:27:29.549716+03	\N
216	\N	20	20	8	4	Well organized	Professional service, on time, and well planned. Minor room for improvement.	t	9	2025-09-19 17:27:29.549959+03	\N
217	\N	21	20	8	5	Fantastic!	Couldn't have asked for a better experience. Will book again next visit.	t	12	2025-09-25 17:27:29.550351+03	\N
218	\N	2	21	8	5	Amazing experience!	Absolutely loved this tour. The guide was knowledgeable and the experience was unforgettable.	f	9	2025-10-07 17:27:29.553641+03	\N
219	\N	3	21	8	5	Highly recommended	Perfect organization, great value for money. Would definitely do this again.	f	13	2025-09-16 17:27:29.554152+03	\N
220	\N	4	21	8	4	Great tour	Really enjoyed the experience. Minor delays but overall fantastic.	t	1	2025-09-19 17:27:29.554397+03	\N
221	\N	5	21	8	5	Exceeded expectations	This tour was even better than described. Authentic and well-organized.	f	15	2025-09-23 17:27:29.554846+03	\N
222	\N	6	21	8	4	Very good	Good experience with professional guide. Worth the price.	f	11	2025-08-06 17:27:29.555344+03	\N
223	\N	7	21	8	5	Outstanding	One of the best tours I've ever taken. Highly professional and informative.	t	4	2025-10-07 17:27:29.555569+03	\N
224	\N	8	21	8	4	Enjoyed it	Nice experience, learned a lot. Would recommend to friends.	t	2	2025-10-18 17:27:29.555815+03	\N
225	\N	9	21	8	5	Perfect!	Everything was perfect from start to finish. Amazing attention to detail.	f	0	2025-10-25 17:27:29.556363+03	\N
226	\N	18	21	8	4	Good value	Fair price for what you get. Guide was very friendly and helpful.	t	14	2025-08-23 17:27:29.556915+03	\N
227	\N	19	21	8	5	Memorable	Created lasting memories. The whole family enjoyed every moment.	t	5	2025-10-10 17:27:29.557409+03	\N
228	\N	20	21	8	4	Well organized	Professional service, on time, and well planned. Minor room for improvement.	f	5	2025-11-02 17:27:29.557632+02	\N
229	\N	21	21	8	5	Fantastic!	Couldn't have asked for a better experience. Will book again next visit.	t	5	2025-08-06 17:27:29.557922+03	\N
230	\N	2	22	8	5	Amazing experience!	Absolutely loved this tour. The guide was knowledgeable and the experience was unforgettable.	f	4	2025-10-21 17:27:29.560851+03	\N
231	\N	3	22	8	5	Highly recommended	Perfect organization, great value for money. Would definitely do this again.	t	14	2025-08-12 17:27:29.561344+03	\N
232	\N	4	22	8	4	Great tour	Really enjoyed the experience. Minor delays but overall fantastic.	t	13	2025-10-31 17:27:29.56157+02	\N
233	\N	5	22	8	5	Exceeded expectations	This tour was even better than described. Authentic and well-organized.	f	13	2025-10-16 17:27:29.56179+03	\N
234	\N	6	22	8	4	Very good	Good experience with professional guide. Worth the price.	t	8	2025-10-03 17:27:29.56203+03	\N
235	\N	7	22	8	5	Outstanding	One of the best tours I've ever taken. Highly professional and informative.	t	11	2025-10-23 17:27:29.562284+03	\N
236	\N	8	22	8	4	Enjoyed it	Nice experience, learned a lot. Would recommend to friends.	f	0	2025-09-06 17:27:29.562547+03	\N
237	\N	9	22	8	5	Perfect!	Everything was perfect from start to finish. Amazing attention to detail.	t	14	2025-08-06 17:27:29.563098+03	\N
238	\N	18	22	8	4	Good value	Fair price for what you get. Guide was very friendly and helpful.	f	2	2025-11-01 17:27:29.563327+02	\N
239	\N	19	22	8	5	Memorable	Created lasting memories. The whole family enjoyed every moment.	f	1	2025-10-22 17:27:29.563572+03	\N
240	\N	20	22	8	4	Well organized	Professional service, on time, and well planned. Minor room for improvement.	f	9	2025-09-03 17:27:29.564144+03	\N
241	\N	21	22	8	5	Fantastic!	Couldn't have asked for a better experience. Will book again next visit.	f	14	2025-10-13 17:27:29.564395+03	\N
\.


--
-- TOC entry 4164 (class 0 OID 26852)
-- Dependencies: 210
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, email, password_hash, full_name, phone, role, email_verified, is_active, created_at, updated_at) FROM stdin;
2	customer@example.com	$2b$12$TxjAN.QLj4nory7k.VFcF.SSwEEM8e1bPYaVVf0vgMQ3QpI.YM0Cy	John Smith	+1-555-0101	CUSTOMER	t	t	2025-11-03 16:32:47.916739+02	\N
3	emily@example.com	$2b$12$pf7Eh3/INPyZERuIq.qzlOFPfJ2RLF2g1dfs.Y6i/9KuzFmLmUNIa	Emily Chen	+86-138-0013-8000	CUSTOMER	t	t	2025-11-03 16:32:47.916739+02	\N
4	marco@example.com	$2b$12$ILR4MFA6swEQZwdPJXCDieFDbmFpS0OGzzthiL1GgfWwzYrHXibaa	Marco Rodriguez	+34-600-123-456	CUSTOMER	t	t	2025-11-03 16:32:47.916739+02	\N
5	liu.wei@example.com	$2b$12$Ng7zK8G4K2JWYQBd1yzRSuEjoy7c9Xt5x3IEJjqMKd5/jcfGfFL4W	Liu Wei	+86-139-0013-9000	CUSTOMER	t	t	2025-11-03 16:32:47.916739+02	\N
6	anna@example.com	$2b$12$ZDY7C7/k05s7PWSnrUolMObubrvBzXbwvxTJidxDBEXP6I2O2OSZi	Anna Larsson	+46-70-123-4567	CUSTOMER	t	t	2025-11-03 16:32:47.916739+02	\N
7	hiroshi@example.com	$2b$12$A7QT1iS9CnnYsZf.O63wJO44osDIkqpJY3EHYehkIg3KrYbdD2k2i	Hiroshi Tanaka	+81-90-1234-5678	CUSTOMER	t	t	2025-11-03 16:32:47.916739+02	\N
8	marie@example.com	$2b$12$y6yQrhrRKdC63F3WVw411../XehT1YCf85SniBnifPcpo18B6Fx6G	Marie Dubois	+33-6-12-34-56-78	CUSTOMER	t	t	2025-11-03 16:32:47.916739+02	\N
9	peter@example.com	$2b$12$MC3K823kTkwuMWxbKrFq..Qt60Mx3jkpIT6q6mu24rhOrvf/jk5Nm	Peter Hansen	+45-20-12-34-56	CUSTOMER	t	t	2025-11-03 16:32:47.916739+02	\N
10	vendor1@beijing-tours.com	$2b$12$lH7lGrwYzw59i.iWbDHTvuOI3LWRkddc6Vcnul./qr4PheYet67MS	Li Ming	\N	VENDOR	t	t	2025-11-03 16:32:47.916739+02	\N
11	vendor2@nordic-adventures.com	$2b$12$QL45I0vHJc7he/bpbPdtau2.xawkQJBpIp7nVgEMx5x/T/3ift2Ly	Erik Andersen	\N	VENDOR	t	t	2025-11-03 16:32:47.916739+02	\N
12	vendor3@shanghai-food.com	$2b$12$GLaOIWvOPJZRmoBylYK1VeNQiNRtZjB7.OgeieJjLoirPi5sheeLu	Wang Mei	\N	VENDOR	t	t	2025-11-03 16:32:47.916739+02	\N
13	vendor4@viking-tours.com	$2b$12$8uzqek5mtJmgt/E8145dbuvrdgCCSTj3T0AaL42jzFHeSvHcPEx8K	Ingrid Olsen	\N	VENDOR	t	t	2025-11-03 16:32:47.916739+02	\N
14	vendor5@dragongate.com	$2b$12$GE18PCi5Gd5M/f34yjRZ9eCTJzFjXiVRNTDSLZlapubHAWoijhEuS	Zhang Lei	\N	VENDOR	t	t	2025-11-03 16:32:47.916739+02	\N
15	vendor6@aurora-exp.com	$2b$12$Mma0fheIXWEYJNl.aqluIedZqD.9d2Rbk8m0Xob61CMAKckS/dCea	Nils Svensson	\N	VENDOR	t	t	2025-11-03 16:32:47.916739+02	\N
17	vendor7@nordic-china-edu.com	$2b$12$b65syBMc.N0mWS21krTU9ec6i3DX.ZPm/SUKZ.jmSmIAW9tMW0jQK	Dr. Anna Chen-Larsson	\N	VENDOR	t	t	2025-11-03 17:27:28.563347+02	\N
18	reviewer8@example.com	$2b$12$tMqmKdAJ.NeMIhJ61ZuXyuWOlBCjXYwNJ4vwBjrRpFI1GXcjcJTVq	Reviewer 8	\N	CUSTOMER	t	t	2025-11-03 17:27:28.563347+02	\N
19	reviewer9@example.com	$2b$12$W8k1Z7lZut1waRzRXm0guuChbVjZ7LL4pz/gjhfz2Amz0ZfI18qiu	Reviewer 9	\N	CUSTOMER	t	t	2025-11-03 17:27:28.563347+02	\N
20	reviewer10@example.com	$2b$12$q5v4gHdXbdvWJpK0ZSAPvuAAOt5aswNnJ3zdl2gce.cbMNe7bzdEu	Reviewer 10	\N	CUSTOMER	t	t	2025-11-03 17:27:28.563347+02	\N
21	reviewer11@example.com	$2b$12$xYOtt64ZmPIGalP7oUtKz..AFk90bcUM8e6iDxGVBp6xHh8sfHDAy	Reviewer 11	\N	CUSTOMER	t	t	2025-11-03 17:27:28.563347+02	\N
1	admin@findtravelmate.com	$2b$12$tfhklecvlbguHUgTUtVL8OebAF0tWHNf4WNEZmHL9mABnywvG0sPG	Travel Admin	\N	ADMIN	t	t	2025-11-03 16:32:47.916739+02	2025-11-03 21:57:24.793316+02
\.


--
-- TOC entry 4170 (class 0 OID 26890)
-- Dependencies: 216
-- Data for Name: vendors; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.vendors (id, user_id, company_name, description, logo_url, commission_rate, is_verified, verified_at, created_at) FROM stdin;
1	10	Beijing Cultural Tours	Authentic Beijing experiences with local experts	https://images.unsplash.com/photo-1502624271-400x400?q=80	24.32	t	2025-11-03 16:32:48.087316+02	2025-11-03 16:32:47.916739+02
2	11	Nordic Adventures	Premium Nordic experiences and 游学 programs	https://images.unsplash.com/photo-1554711245-400x400?q=80	17.52	t	2025-11-03 16:32:48.258006+02	2025-11-03 16:32:47.916739+02
3	12	Shanghai Food Masters	Culinary journeys through Shanghai's best flavors	https://images.unsplash.com/photo-1527017372-400x400?q=80	15.51	t	2025-11-03 16:32:48.424113+02	2025-11-03 16:32:47.916739+02
4	13	Viking Heritage Tours	Historical and cultural tours across Scandinavia	https://images.unsplash.com/photo-1531565402-400x400?q=80	24.58	t	2025-11-03 16:32:48.590169+02	2025-11-03 16:32:47.916739+02
5	14	Dragon Gate Travel	Luxury travel experiences across China	https://images.unsplash.com/photo-1531622888-400x400?q=80	19.71	t	2025-11-03 16:32:48.755606+02	2025-11-03 16:32:47.916739+02
6	15	Aurora Experience	Northern Lights and Arctic adventures	https://images.unsplash.com/photo-1575299192-400x400?q=80	23.53	t	2025-11-03 16:32:48.921892+02	2025-11-03 16:32:47.916739+02
8	17	Nordic Education & China Cultural Exchange	Specializing in educational tours and cultural exchange programs between Nordic countries and China. Expert in Nordic study tours and authentic Chinese cultural experiences.	https://picsum.photos/seed/nordic-china-edu-logo/400/400	18.50	t	2025-11-03 17:27:28.736193+02	2025-11-03 17:27:28.563347+02
\.


--
-- TOC entry 4201 (class 0 OID 27166)
-- Dependencies: 247
-- Data for Name: wishlist; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.wishlist (user_id, activity_id, created_at) FROM stdin;
\.


--
-- TOC entry 4264 (class 0 OID 0)
-- Dependencies: 221
-- Name: activities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.activities_id_seq', 1, false);


--
-- TOC entry 4265 (class 0 OID 0)
-- Dependencies: 241
-- Name: activity_add_ons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.activity_add_ons_id_seq', 1, false);


--
-- TOC entry 4266 (class 0 OID 0)
-- Dependencies: 266
-- Name: activity_addon_translations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.activity_addon_translations_id_seq', 1, false);


--
-- TOC entry 4267 (class 0 OID 0)
-- Dependencies: 260
-- Name: activity_faq_translations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.activity_faq_translations_id_seq', 1, false);


--
-- TOC entry 4268 (class 0 OID 0)
-- Dependencies: 231
-- Name: activity_faqs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.activity_faqs_id_seq', 1, false);


--
-- TOC entry 4269 (class 0 OID 0)
-- Dependencies: 256
-- Name: activity_highlight_translations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.activity_highlight_translations_id_seq', 1, false);


--
-- TOC entry 4270 (class 0 OID 0)
-- Dependencies: 227
-- Name: activity_highlights_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.activity_highlights_id_seq', 1, false);


--
-- TOC entry 4271 (class 0 OID 0)
-- Dependencies: 223
-- Name: activity_images_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.activity_images_id_seq', 1, false);


--
-- TOC entry 4272 (class 0 OID 0)
-- Dependencies: 258
-- Name: activity_include_translations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.activity_include_translations_id_seq', 1, false);


--
-- TOC entry 4273 (class 0 OID 0)
-- Dependencies: 229
-- Name: activity_includes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.activity_includes_id_seq', 1, false);


--
-- TOC entry 4274 (class 0 OID 0)
-- Dependencies: 264
-- Name: activity_pricing_tier_translations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.activity_pricing_tier_translations_id_seq', 1, false);


--
-- TOC entry 4275 (class 0 OID 0)
-- Dependencies: 239
-- Name: activity_pricing_tiers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.activity_pricing_tiers_id_seq', 1, false);


--
-- TOC entry 4276 (class 0 OID 0)
-- Dependencies: 237
-- Name: activity_time_slots_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.activity_time_slots_id_seq', 1, false);


--
-- TOC entry 4277 (class 0 OID 0)
-- Dependencies: 262
-- Name: activity_timeline_translations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.activity_timeline_translations_id_seq', 1, false);


--
-- TOC entry 4278 (class 0 OID 0)
-- Dependencies: 235
-- Name: activity_timelines_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.activity_timelines_id_seq', 1, false);


--
-- TOC entry 4279 (class 0 OID 0)
-- Dependencies: 248
-- Name: activity_translations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.activity_translations_id_seq', 1, true);


--
-- TOC entry 4280 (class 0 OID 0)
-- Dependencies: 245
-- Name: availability_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.availability_id_seq', 1, false);


--
-- TOC entry 4281 (class 0 OID 0)
-- Dependencies: 243
-- Name: bookings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.bookings_id_seq', 1, false);


--
-- TOC entry 4282 (class 0 OID 0)
-- Dependencies: 252
-- Name: cart_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cart_items_id_seq', 1, false);


--
-- TOC entry 4283 (class 0 OID 0)
-- Dependencies: 211
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.categories_id_seq', 1, false);


--
-- TOC entry 4284 (class 0 OID 0)
-- Dependencies: 217
-- Name: category_translations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.category_translations_id_seq', 30, true);


--
-- TOC entry 4285 (class 0 OID 0)
-- Dependencies: 219
-- Name: destination_translations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.destination_translations_id_seq', 1, false);


--
-- TOC entry 4286 (class 0 OID 0)
-- Dependencies: 213
-- Name: destinations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.destinations_id_seq', 1, false);


--
-- TOC entry 4287 (class 0 OID 0)
-- Dependencies: 250
-- Name: meeting_point_photos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.meeting_point_photos_id_seq', 1, false);


--
-- TOC entry 4288 (class 0 OID 0)
-- Dependencies: 268
-- Name: meeting_point_translations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.meeting_point_translations_id_seq', 1, false);


--
-- TOC entry 4289 (class 0 OID 0)
-- Dependencies: 233
-- Name: meeting_points_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.meeting_points_id_seq', 1, false);


--
-- TOC entry 4290 (class 0 OID 0)
-- Dependencies: 272
-- Name: review_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.review_categories_id_seq', 1, false);


--
-- TOC entry 4291 (class 0 OID 0)
-- Dependencies: 270
-- Name: review_images_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.review_images_id_seq', 1, false);


--
-- TOC entry 4292 (class 0 OID 0)
-- Dependencies: 254
-- Name: reviews_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.reviews_id_seq', 1, false);


--
-- TOC entry 4293 (class 0 OID 0)
-- Dependencies: 209
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- TOC entry 4294 (class 0 OID 0)
-- Dependencies: 215
-- Name: vendors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.vendors_id_seq', 1, false);


--
-- TOC entry 3877 (class 2606 OID 26948)
-- Name: activities pk_activities; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT pk_activities PRIMARY KEY (id);


--
-- TOC entry 3910 (class 2606 OID 27114)
-- Name: activity_add_ons pk_activity_add_ons; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_add_ons
    ADD CONSTRAINT pk_activity_add_ons PRIMARY KEY (id);


--
-- TOC entry 3968 (class 2606 OID 27368)
-- Name: activity_addon_translations pk_activity_addon_translations; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_addon_translations
    ADD CONSTRAINT pk_activity_addon_translations PRIMARY KEY (id);


--
-- TOC entry 3882 (class 2606 OID 26975)
-- Name: activity_categories pk_activity_categories; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_categories
    ADD CONSTRAINT pk_activity_categories PRIMARY KEY (activity_id, category_id);


--
-- TOC entry 3884 (class 2606 OID 26990)
-- Name: activity_destinations pk_activity_destinations; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_destinations
    ADD CONSTRAINT pk_activity_destinations PRIMARY KEY (activity_id, destination_id);


--
-- TOC entry 3953 (class 2606 OID 27317)
-- Name: activity_faq_translations pk_activity_faq_translations; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_faq_translations
    ADD CONSTRAINT pk_activity_faq_translations PRIMARY KEY (id);


--
-- TOC entry 3893 (class 2606 OID 27039)
-- Name: activity_faqs pk_activity_faqs; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_faqs
    ADD CONSTRAINT pk_activity_faqs PRIMARY KEY (id);


--
-- TOC entry 3943 (class 2606 OID 27283)
-- Name: activity_highlight_translations pk_activity_highlight_translations; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_highlight_translations
    ADD CONSTRAINT pk_activity_highlight_translations PRIMARY KEY (id);


--
-- TOC entry 3887 (class 2606 OID 27009)
-- Name: activity_highlights pk_activity_highlights; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_highlights
    ADD CONSTRAINT pk_activity_highlights PRIMARY KEY (id);


--
-- TOC entry 3880 (class 2606 OID 26964)
-- Name: activity_images pk_activity_images; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_images
    ADD CONSTRAINT pk_activity_images PRIMARY KEY (id);


--
-- TOC entry 3948 (class 2606 OID 27300)
-- Name: activity_include_translations pk_activity_include_translations; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_include_translations
    ADD CONSTRAINT pk_activity_include_translations PRIMARY KEY (id);


--
-- TOC entry 3890 (class 2606 OID 27024)
-- Name: activity_includes pk_activity_includes; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_includes
    ADD CONSTRAINT pk_activity_includes PRIMARY KEY (id);


--
-- TOC entry 3963 (class 2606 OID 27351)
-- Name: activity_pricing_tier_translations pk_activity_pricing_tier_translations; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_pricing_tier_translations
    ADD CONSTRAINT pk_activity_pricing_tier_translations PRIMARY KEY (id);


--
-- TOC entry 3907 (class 2606 OID 27099)
-- Name: activity_pricing_tiers pk_activity_pricing_tiers; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_pricing_tiers
    ADD CONSTRAINT pk_activity_pricing_tiers PRIMARY KEY (id);


--
-- TOC entry 3904 (class 2606 OID 27084)
-- Name: activity_time_slots pk_activity_time_slots; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_time_slots
    ADD CONSTRAINT pk_activity_time_slots PRIMARY KEY (id);


--
-- TOC entry 3958 (class 2606 OID 27334)
-- Name: activity_timeline_translations pk_activity_timeline_translations; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_timeline_translations
    ADD CONSTRAINT pk_activity_timeline_translations PRIMARY KEY (id);


--
-- TOC entry 3901 (class 2606 OID 27071)
-- Name: activity_timelines pk_activity_timelines; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_timelines
    ADD CONSTRAINT pk_activity_timelines PRIMARY KEY (id);


--
-- TOC entry 3927 (class 2606 OID 27191)
-- Name: activity_translations pk_activity_translations; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_translations
    ADD CONSTRAINT pk_activity_translations PRIMARY KEY (id);


--
-- TOC entry 3922 (class 2606 OID 27157)
-- Name: availability pk_availability; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.availability
    ADD CONSTRAINT pk_availability PRIMARY KEY (id);


--
-- TOC entry 3917 (class 2606 OID 27130)
-- Name: bookings pk_bookings; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT pk_bookings PRIMARY KEY (id);


--
-- TOC entry 3937 (class 2606 OID 27224)
-- Name: cart_items pk_cart_items; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT pk_cart_items PRIMARY KEY (id);


--
-- TOC entry 3854 (class 2606 OID 26869)
-- Name: categories pk_categories; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT pk_categories PRIMARY KEY (id);


--
-- TOC entry 3866 (class 2606 OID 26914)
-- Name: category_translations pk_category_translations; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.category_translations
    ADD CONSTRAINT pk_category_translations PRIMARY KEY (id);


--
-- TOC entry 3871 (class 2606 OID 26930)
-- Name: destination_translations pk_destination_translations; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.destination_translations
    ADD CONSTRAINT pk_destination_translations PRIMARY KEY (id);


--
-- TOC entry 3858 (class 2606 OID 26886)
-- Name: destinations pk_destinations; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.destinations
    ADD CONSTRAINT pk_destinations PRIMARY KEY (id);


--
-- TOC entry 3932 (class 2606 OID 27208)
-- Name: meeting_point_photos pk_meeting_point_photos; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meeting_point_photos
    ADD CONSTRAINT pk_meeting_point_photos PRIMARY KEY (id);


--
-- TOC entry 3973 (class 2606 OID 27385)
-- Name: meeting_point_translations pk_meeting_point_translations; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meeting_point_translations
    ADD CONSTRAINT pk_meeting_point_translations PRIMARY KEY (id);


--
-- TOC entry 3896 (class 2606 OID 27054)
-- Name: meeting_points pk_meeting_points; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meeting_points
    ADD CONSTRAINT pk_meeting_points PRIMARY KEY (id);


--
-- TOC entry 3981 (class 2606 OID 27416)
-- Name: review_categories pk_review_categories; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.review_categories
    ADD CONSTRAINT pk_review_categories PRIMARY KEY (id);


--
-- TOC entry 3978 (class 2606 OID 27402)
-- Name: review_images pk_review_images; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.review_images
    ADD CONSTRAINT pk_review_images PRIMARY KEY (id);


--
-- TOC entry 3940 (class 2606 OID 27253)
-- Name: reviews pk_reviews; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT pk_reviews PRIMARY KEY (id);


--
-- TOC entry 3850 (class 2606 OID 26860)
-- Name: users pk_users; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT pk_users PRIMARY KEY (id);


--
-- TOC entry 3861 (class 2606 OID 26898)
-- Name: vendors pk_vendors; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vendors
    ADD CONSTRAINT pk_vendors PRIMARY KEY (id);


--
-- TOC entry 3924 (class 2606 OID 27171)
-- Name: wishlist pk_wishlist; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.wishlist
    ADD CONSTRAINT pk_wishlist PRIMARY KEY (user_id, activity_id);


--
-- TOC entry 3929 (class 2606 OID 27193)
-- Name: activity_translations uq_activity_language; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_translations
    ADD CONSTRAINT uq_activity_language UNIQUE (activity_id, language);


--
-- TOC entry 3970 (class 2606 OID 27370)
-- Name: activity_addon_translations uq_addon_language; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_addon_translations
    ADD CONSTRAINT uq_addon_language UNIQUE (addon_id, language);


--
-- TOC entry 3868 (class 2606 OID 26916)
-- Name: category_translations uq_category_language; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.category_translations
    ADD CONSTRAINT uq_category_language UNIQUE (category_id, language);


--
-- TOC entry 3873 (class 2606 OID 26932)
-- Name: destination_translations uq_destination_language; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.destination_translations
    ADD CONSTRAINT uq_destination_language UNIQUE (destination_id, language);


--
-- TOC entry 3955 (class 2606 OID 27319)
-- Name: activity_faq_translations uq_faq_language; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_faq_translations
    ADD CONSTRAINT uq_faq_language UNIQUE (faq_id, language);


--
-- TOC entry 3945 (class 2606 OID 27285)
-- Name: activity_highlight_translations uq_highlight_language; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_highlight_translations
    ADD CONSTRAINT uq_highlight_language UNIQUE (highlight_id, language);


--
-- TOC entry 3950 (class 2606 OID 27302)
-- Name: activity_include_translations uq_include_language; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_include_translations
    ADD CONSTRAINT uq_include_language UNIQUE (include_id, language);


--
-- TOC entry 3975 (class 2606 OID 27387)
-- Name: meeting_point_translations uq_meeting_point_language; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meeting_point_translations
    ADD CONSTRAINT uq_meeting_point_language UNIQUE (meeting_point_id, language);


--
-- TOC entry 3898 (class 2606 OID 27056)
-- Name: meeting_points uq_meeting_points_activity_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meeting_points
    ADD CONSTRAINT uq_meeting_points_activity_id UNIQUE (activity_id);


--
-- TOC entry 3965 (class 2606 OID 27353)
-- Name: activity_pricing_tier_translations uq_pricing_tier_language; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_pricing_tier_translations
    ADD CONSTRAINT uq_pricing_tier_language UNIQUE (pricing_tier_id, language);


--
-- TOC entry 3960 (class 2606 OID 27336)
-- Name: activity_timeline_translations uq_timeline_language; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_timeline_translations
    ADD CONSTRAINT uq_timeline_language UNIQUE (timeline_id, language);


--
-- TOC entry 3863 (class 2606 OID 26900)
-- Name: vendors uq_vendors_user_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vendors
    ADD CONSTRAINT uq_vendors_user_id UNIQUE (user_id);


--
-- TOC entry 3918 (class 1259 OID 27165)
-- Name: idx_availability; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX idx_availability ON public.availability USING btree (activity_id, date, start_time);


--
-- TOC entry 3919 (class 1259 OID 27163)
-- Name: idx_availability_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_availability_date ON public.availability USING btree (date);


--
-- TOC entry 3911 (class 1259 OID 27147)
-- Name: idx_booking_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_booking_date ON public.bookings USING btree (booking_date);


--
-- TOC entry 3933 (class 1259 OID 27241)
-- Name: idx_cart_session; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_cart_session ON public.cart_items USING btree (session_id);


--
-- TOC entry 3912 (class 1259 OID 27148)
-- Name: idx_user_bookings; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_user_bookings ON public.bookings USING btree (user_id, status);


--
-- TOC entry 3913 (class 1259 OID 27149)
-- Name: idx_vendor_bookings; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_vendor_bookings ON public.bookings USING btree (vendor_id, booking_date);


--
-- TOC entry 3874 (class 1259 OID 26955)
-- Name: ix_activities_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activities_id ON public.activities USING btree (id);


--
-- TOC entry 3875 (class 1259 OID 26954)
-- Name: ix_activities_slug; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_activities_slug ON public.activities USING btree (slug);


--
-- TOC entry 3908 (class 1259 OID 27120)
-- Name: ix_activity_add_ons_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_add_ons_id ON public.activity_add_ons USING btree (id);


--
-- TOC entry 3966 (class 1259 OID 27376)
-- Name: ix_activity_addon_translations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_addon_translations_id ON public.activity_addon_translations USING btree (id);


--
-- TOC entry 3951 (class 1259 OID 27325)
-- Name: ix_activity_faq_translations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_faq_translations_id ON public.activity_faq_translations USING btree (id);


--
-- TOC entry 3891 (class 1259 OID 27045)
-- Name: ix_activity_faqs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_faqs_id ON public.activity_faqs USING btree (id);


--
-- TOC entry 3941 (class 1259 OID 27291)
-- Name: ix_activity_highlight_translations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_highlight_translations_id ON public.activity_highlight_translations USING btree (id);


--
-- TOC entry 3885 (class 1259 OID 27015)
-- Name: ix_activity_highlights_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_highlights_id ON public.activity_highlights USING btree (id);


--
-- TOC entry 3878 (class 1259 OID 26970)
-- Name: ix_activity_images_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_images_id ON public.activity_images USING btree (id);


--
-- TOC entry 3946 (class 1259 OID 27308)
-- Name: ix_activity_include_translations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_include_translations_id ON public.activity_include_translations USING btree (id);


--
-- TOC entry 3888 (class 1259 OID 27030)
-- Name: ix_activity_includes_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_includes_id ON public.activity_includes USING btree (id);


--
-- TOC entry 3961 (class 1259 OID 27359)
-- Name: ix_activity_pricing_tier_translations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_pricing_tier_translations_id ON public.activity_pricing_tier_translations USING btree (id);


--
-- TOC entry 3905 (class 1259 OID 27105)
-- Name: ix_activity_pricing_tiers_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_pricing_tiers_id ON public.activity_pricing_tiers USING btree (id);


--
-- TOC entry 3902 (class 1259 OID 27090)
-- Name: ix_activity_time_slots_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_time_slots_id ON public.activity_time_slots USING btree (id);


--
-- TOC entry 3956 (class 1259 OID 27342)
-- Name: ix_activity_timeline_translations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_timeline_translations_id ON public.activity_timeline_translations USING btree (id);


--
-- TOC entry 3899 (class 1259 OID 27077)
-- Name: ix_activity_timelines_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_timelines_id ON public.activity_timelines USING btree (id);


--
-- TOC entry 3925 (class 1259 OID 27199)
-- Name: ix_activity_translations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_translations_id ON public.activity_translations USING btree (id);


--
-- TOC entry 3920 (class 1259 OID 27164)
-- Name: ix_availability_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_availability_id ON public.availability USING btree (id);


--
-- TOC entry 3914 (class 1259 OID 27150)
-- Name: ix_bookings_booking_ref; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_bookings_booking_ref ON public.bookings USING btree (booking_ref);


--
-- TOC entry 3915 (class 1259 OID 27146)
-- Name: ix_bookings_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_bookings_id ON public.bookings USING btree (id);


--
-- TOC entry 3934 (class 1259 OID 27240)
-- Name: ix_cart_items_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_cart_items_id ON public.cart_items USING btree (id);


--
-- TOC entry 3935 (class 1259 OID 27242)
-- Name: ix_cart_items_session_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_cart_items_session_id ON public.cart_items USING btree (session_id);


--
-- TOC entry 3851 (class 1259 OID 26876)
-- Name: ix_categories_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_categories_id ON public.categories USING btree (id);


--
-- TOC entry 3852 (class 1259 OID 26875)
-- Name: ix_categories_slug; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_categories_slug ON public.categories USING btree (slug);


--
-- TOC entry 3864 (class 1259 OID 26922)
-- Name: ix_category_translations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_category_translations_id ON public.category_translations USING btree (id);


--
-- TOC entry 3869 (class 1259 OID 26938)
-- Name: ix_destination_translations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_destination_translations_id ON public.destination_translations USING btree (id);


--
-- TOC entry 3855 (class 1259 OID 26887)
-- Name: ix_destinations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_destinations_id ON public.destinations USING btree (id);


--
-- TOC entry 3856 (class 1259 OID 26888)
-- Name: ix_destinations_slug; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_destinations_slug ON public.destinations USING btree (slug);


--
-- TOC entry 3930 (class 1259 OID 27214)
-- Name: ix_meeting_point_photos_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_meeting_point_photos_id ON public.meeting_point_photos USING btree (id);


--
-- TOC entry 3971 (class 1259 OID 27393)
-- Name: ix_meeting_point_translations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_meeting_point_translations_id ON public.meeting_point_translations USING btree (id);


--
-- TOC entry 3894 (class 1259 OID 27062)
-- Name: ix_meeting_points_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_meeting_points_id ON public.meeting_points USING btree (id);


--
-- TOC entry 3979 (class 1259 OID 27422)
-- Name: ix_review_categories_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_review_categories_id ON public.review_categories USING btree (id);


--
-- TOC entry 3976 (class 1259 OID 27408)
-- Name: ix_review_images_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_review_images_id ON public.review_images USING btree (id);


--
-- TOC entry 3938 (class 1259 OID 27274)
-- Name: ix_reviews_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_reviews_id ON public.reviews USING btree (id);


--
-- TOC entry 3847 (class 1259 OID 26862)
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- TOC entry 3848 (class 1259 OID 26861)
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- TOC entry 3859 (class 1259 OID 26906)
-- Name: ix_vendors_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_vendors_id ON public.vendors USING btree (id);


--
-- TOC entry 3986 (class 2606 OID 26949)
-- Name: activities fk_activities_vendor_id_vendors; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT fk_activities_vendor_id_vendors FOREIGN KEY (vendor_id) REFERENCES public.vendors(id) ON DELETE CASCADE;


--
-- TOC entry 3999 (class 2606 OID 27115)
-- Name: activity_add_ons fk_activity_add_ons_activity_id_activities; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_add_ons
    ADD CONSTRAINT fk_activity_add_ons_activity_id_activities FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- TOC entry 4020 (class 2606 OID 27371)
-- Name: activity_addon_translations fk_activity_addon_translations_addon_id_activity_add_ons; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_addon_translations
    ADD CONSTRAINT fk_activity_addon_translations_addon_id_activity_add_ons FOREIGN KEY (addon_id) REFERENCES public.activity_add_ons(id) ON DELETE CASCADE;


--
-- TOC entry 3988 (class 2606 OID 26976)
-- Name: activity_categories fk_activity_categories_activity_id_activities; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_categories
    ADD CONSTRAINT fk_activity_categories_activity_id_activities FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- TOC entry 3989 (class 2606 OID 26981)
-- Name: activity_categories fk_activity_categories_category_id_categories; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_categories
    ADD CONSTRAINT fk_activity_categories_category_id_categories FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE CASCADE;


--
-- TOC entry 3990 (class 2606 OID 26991)
-- Name: activity_destinations fk_activity_destinations_activity_id_activities; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_destinations
    ADD CONSTRAINT fk_activity_destinations_activity_id_activities FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- TOC entry 3991 (class 2606 OID 26996)
-- Name: activity_destinations fk_activity_destinations_destination_id_destinations; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_destinations
    ADD CONSTRAINT fk_activity_destinations_destination_id_destinations FOREIGN KEY (destination_id) REFERENCES public.destinations(id) ON DELETE CASCADE;


--
-- TOC entry 4017 (class 2606 OID 27320)
-- Name: activity_faq_translations fk_activity_faq_translations_faq_id_activity_faqs; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_faq_translations
    ADD CONSTRAINT fk_activity_faq_translations_faq_id_activity_faqs FOREIGN KEY (faq_id) REFERENCES public.activity_faqs(id) ON DELETE CASCADE;


--
-- TOC entry 3994 (class 2606 OID 27040)
-- Name: activity_faqs fk_activity_faqs_activity_id_activities; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_faqs
    ADD CONSTRAINT fk_activity_faqs_activity_id_activities FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- TOC entry 4015 (class 2606 OID 27286)
-- Name: activity_highlight_translations fk_activity_highlight_translations_highlight_id_activit_e9a3; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_highlight_translations
    ADD CONSTRAINT fk_activity_highlight_translations_highlight_id_activit_e9a3 FOREIGN KEY (highlight_id) REFERENCES public.activity_highlights(id) ON DELETE CASCADE;


--
-- TOC entry 3992 (class 2606 OID 27010)
-- Name: activity_highlights fk_activity_highlights_activity_id_activities; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_highlights
    ADD CONSTRAINT fk_activity_highlights_activity_id_activities FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- TOC entry 3987 (class 2606 OID 26965)
-- Name: activity_images fk_activity_images_activity_id_activities; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_images
    ADD CONSTRAINT fk_activity_images_activity_id_activities FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- TOC entry 4016 (class 2606 OID 27303)
-- Name: activity_include_translations fk_activity_include_translations_include_id_activity_includes; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_include_translations
    ADD CONSTRAINT fk_activity_include_translations_include_id_activity_includes FOREIGN KEY (include_id) REFERENCES public.activity_includes(id) ON DELETE CASCADE;


--
-- TOC entry 3993 (class 2606 OID 27025)
-- Name: activity_includes fk_activity_includes_activity_id_activities; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_includes
    ADD CONSTRAINT fk_activity_includes_activity_id_activities FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- TOC entry 4019 (class 2606 OID 27354)
-- Name: activity_pricing_tier_translations fk_activity_pricing_tier_translations_pricing_tier_id_a_34c1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_pricing_tier_translations
    ADD CONSTRAINT fk_activity_pricing_tier_translations_pricing_tier_id_a_34c1 FOREIGN KEY (pricing_tier_id) REFERENCES public.activity_pricing_tiers(id) ON DELETE CASCADE;


--
-- TOC entry 3998 (class 2606 OID 27100)
-- Name: activity_pricing_tiers fk_activity_pricing_tiers_activity_id_activities; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_pricing_tiers
    ADD CONSTRAINT fk_activity_pricing_tiers_activity_id_activities FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- TOC entry 3997 (class 2606 OID 27085)
-- Name: activity_time_slots fk_activity_time_slots_activity_id_activities; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_time_slots
    ADD CONSTRAINT fk_activity_time_slots_activity_id_activities FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- TOC entry 4018 (class 2606 OID 27337)
-- Name: activity_timeline_translations fk_activity_timeline_translations_timeline_id_activity__fd8f; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_timeline_translations
    ADD CONSTRAINT fk_activity_timeline_translations_timeline_id_activity__fd8f FOREIGN KEY (timeline_id) REFERENCES public.activity_timelines(id) ON DELETE CASCADE;


--
-- TOC entry 3996 (class 2606 OID 27072)
-- Name: activity_timelines fk_activity_timelines_activity_id_activities; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_timelines
    ADD CONSTRAINT fk_activity_timelines_activity_id_activities FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- TOC entry 4006 (class 2606 OID 27194)
-- Name: activity_translations fk_activity_translations_activity_id_activities; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_translations
    ADD CONSTRAINT fk_activity_translations_activity_id_activities FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- TOC entry 4003 (class 2606 OID 27158)
-- Name: availability fk_availability_activity_id_activities; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.availability
    ADD CONSTRAINT fk_availability_activity_id_activities FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- TOC entry 4001 (class 2606 OID 27136)
-- Name: bookings fk_bookings_activity_id_activities; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT fk_bookings_activity_id_activities FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- TOC entry 4000 (class 2606 OID 27131)
-- Name: bookings fk_bookings_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT fk_bookings_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- TOC entry 4002 (class 2606 OID 27141)
-- Name: bookings fk_bookings_vendor_id_vendors; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT fk_bookings_vendor_id_vendors FOREIGN KEY (vendor_id) REFERENCES public.vendors(id) ON DELETE CASCADE;


--
-- TOC entry 4008 (class 2606 OID 27225)
-- Name: cart_items fk_cart_items_activity_id_activities; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT fk_cart_items_activity_id_activities FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- TOC entry 4010 (class 2606 OID 27235)
-- Name: cart_items fk_cart_items_pricing_tier_id_activity_pricing_tiers; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT fk_cart_items_pricing_tier_id_activity_pricing_tiers FOREIGN KEY (pricing_tier_id) REFERENCES public.activity_pricing_tiers(id) ON DELETE SET NULL;


--
-- TOC entry 4009 (class 2606 OID 27230)
-- Name: cart_items fk_cart_items_time_slot_id_activity_time_slots; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT fk_cart_items_time_slot_id_activity_time_slots FOREIGN KEY (time_slot_id) REFERENCES public.activity_time_slots(id) ON DELETE SET NULL;


--
-- TOC entry 3982 (class 2606 OID 26870)
-- Name: categories fk_categories_parent_id_categories; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT fk_categories_parent_id_categories FOREIGN KEY (parent_id) REFERENCES public.categories(id);


--
-- TOC entry 3984 (class 2606 OID 26917)
-- Name: category_translations fk_category_translations_category_id_categories; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.category_translations
    ADD CONSTRAINT fk_category_translations_category_id_categories FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE CASCADE;


--
-- TOC entry 3985 (class 2606 OID 26933)
-- Name: destination_translations fk_destination_translations_destination_id_destinations; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.destination_translations
    ADD CONSTRAINT fk_destination_translations_destination_id_destinations FOREIGN KEY (destination_id) REFERENCES public.destinations(id) ON DELETE CASCADE;


--
-- TOC entry 4007 (class 2606 OID 27209)
-- Name: meeting_point_photos fk_meeting_point_photos_meeting_point_id_meeting_points; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meeting_point_photos
    ADD CONSTRAINT fk_meeting_point_photos_meeting_point_id_meeting_points FOREIGN KEY (meeting_point_id) REFERENCES public.meeting_points(id) ON DELETE CASCADE;


--
-- TOC entry 4021 (class 2606 OID 27388)
-- Name: meeting_point_translations fk_meeting_point_translations_meeting_point_id_meeting_points; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meeting_point_translations
    ADD CONSTRAINT fk_meeting_point_translations_meeting_point_id_meeting_points FOREIGN KEY (meeting_point_id) REFERENCES public.meeting_points(id) ON DELETE CASCADE;


--
-- TOC entry 3995 (class 2606 OID 27057)
-- Name: meeting_points fk_meeting_points_activity_id_activities; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meeting_points
    ADD CONSTRAINT fk_meeting_points_activity_id_activities FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- TOC entry 4023 (class 2606 OID 27417)
-- Name: review_categories fk_review_categories_review_id_reviews; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.review_categories
    ADD CONSTRAINT fk_review_categories_review_id_reviews FOREIGN KEY (review_id) REFERENCES public.reviews(id) ON DELETE CASCADE;


--
-- TOC entry 4022 (class 2606 OID 27403)
-- Name: review_images fk_review_images_review_id_reviews; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.review_images
    ADD CONSTRAINT fk_review_images_review_id_reviews FOREIGN KEY (review_id) REFERENCES public.reviews(id) ON DELETE CASCADE;


--
-- TOC entry 4013 (class 2606 OID 27264)
-- Name: reviews fk_reviews_activity_id_activities; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT fk_reviews_activity_id_activities FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- TOC entry 4011 (class 2606 OID 27254)
-- Name: reviews fk_reviews_booking_id_bookings; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT fk_reviews_booking_id_bookings FOREIGN KEY (booking_id) REFERENCES public.bookings(id) ON DELETE CASCADE;


--
-- TOC entry 4012 (class 2606 OID 27259)
-- Name: reviews fk_reviews_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT fk_reviews_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4014 (class 2606 OID 27269)
-- Name: reviews fk_reviews_vendor_id_vendors; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT fk_reviews_vendor_id_vendors FOREIGN KEY (vendor_id) REFERENCES public.vendors(id) ON DELETE CASCADE;


--
-- TOC entry 3983 (class 2606 OID 26901)
-- Name: vendors fk_vendors_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vendors
    ADD CONSTRAINT fk_vendors_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4005 (class 2606 OID 27177)
-- Name: wishlist fk_wishlist_activity_id_activities; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.wishlist
    ADD CONSTRAINT fk_wishlist_activity_id_activities FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- TOC entry 4004 (class 2606 OID 27172)
-- Name: wishlist fk_wishlist_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.wishlist
    ADD CONSTRAINT fk_wishlist_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


-- Completed on 2025-11-04 22:45:58 EET

--
-- PostgreSQL database dump complete
--

\unrestrict eChgyH9isuHeYMd4naDpgj6avArun2IDqZC5J11EeoVNZo3asgry3jfFfK4TUWZ

