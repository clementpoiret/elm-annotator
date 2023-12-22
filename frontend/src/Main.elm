module Main exposing (..)

import Browser
import Element exposing (..)
import Element.Background as Background
import Element.Border as Border exposing (shadow)
import Element.Font as Font
import Element.Input as Input
import Html exposing (Html)
import Http



-- MAIN


main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }



-- MODEL


type Model
    = Default
    | Success String


init : () -> ( Model, Cmd Msg )
init _ =
    ( Default
    , Cmd.none
    )



-- UPDATE


type Msg
    = Clicked


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Clicked ->
            ( Success "Clicked", Cmd.none )



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- VIEW


bgColor : Color
bgColor =
    rgb255 245 245 245


darkBgColor : Color
darkBgColor =
    rgb255 0 0 0


lightBgColor : Color
lightBgColor =
    rgb255 255 255 255


borderColor : Color
borderColor =
    rgb255 0 0 0


shadowColor : Color
shadowColor =
    rgb255 93 93 93


primaryColor : Color
primaryColor =
    rgb255 159 233 110


secondaryColor : Color
secondaryColor =
    rgb255 164 167 246


redColor : Color
redColor =
    rgb255 202 46 85


view : Model -> Html Msg
view model =
    layout
        [ width fill
        , height fill
        , Background.color bgColor
        , Font.family
            [ Font.typeface "IBM Plex Mono"
            , Font.typeface "monospace"
            ]
        , paddingXY 32 16
        ]
    <|
        column
            [ width fill
            , height fill
            ]
            [ header
            , row
                [ height fill
                , width fill
                , spacing 32
                , paddingXY 0 16
                ]
                [ sidebar
                , mainContainer
                ]
            ]


header : Element msg
header =
    row
        [ width fill
        , height <| px 64
        ]
        [ row
            [ spacing 16
            , Font.bold
            , Font.size 32
            , alignLeft
            ]
            [ el
                [ width <| px 4
                , height <| px 32
                , Background.color <| rgb 0 0 0
                ]
                (text "")
            , text "Elm Annotator"
            ]
        ]


sidebar : Element msg
sidebar =
    column
        [ height fill
        , width <| px 256
        , spacing 32
        ]
        [ el
            [ height <| px 128
            , width fill
            , Border.width 2
            , Border.color borderColor
            , Background.color primaryColor
            , shadow
                { blur = 0.0
                , color = shadowColor
                , offset = ( 8.0, 8.0 )
                , size = 0.0
                }
            , Border.rounded 16
            ]
            (text "")
        , el
            [ height fill
            , width fill
            , Border.width 2
            , Border.color borderColor
            , Background.color darkBgColor
            , shadow
                { blur = 0.0
                , color = shadowColor
                , offset = ( 8.0, 8.0 )
                , size = 0.0
                }
            , Border.rounded 16
            ]
            (text "")
        ]


button : Color -> String -> Element Msg
button color label =
    Input.button
        [ Background.color color
        , paddingXY 16 8
        , Border.rounded 32
        , Border.color borderColor
        , Border.width 2
        , shadow
            { blur = 0.0
            , color = shadowColor
            , offset = ( 4.0, 4.0 )
            , size = 0.0
            }
        ]
        { onPress = Just Clicked
        , label = text label
        }


mainContainer : Element Msg
mainContainer =
    column
        [ height fill
        , width fill
        , Border.rounded 16
        ]
        [ el [ height fill ] <|
            text ""
        , row
            [ height <| px 32
            , alignRight
            , spacing 16
            ]
            [ button redColor "Nooope"
            , button lightBgColor "Maybe"
            , button secondaryColor "Yay!"
            ]
        ]
