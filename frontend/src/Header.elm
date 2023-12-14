module Header exposing (header)

import Element exposing (..)
import Element.Background as Background
import Element.Border as Border
import Element.Font as Font
import Html exposing (Html)


header : Element msg
header =
    el
        [ width fill
        , height <| px 128
        , padding 32
        , Font.family
            [ Font.typeface "IBM Plex Mono"
            , Font.typeface "monospace"
            ]
        , Font.bold
        ]
    <|
        el [ centerY ] <|
            row
                [ centerX
                , centerY
                , spacing 8
                , Font.size 32
                ]
                [ el
                    [ centerX
                    , centerY
                    , width <| px 4
                    , height <| px 32
                    , Background.color <| rgb 0 0 0
                    ]
                  <|
                    text ""
                , text "Elm Annotator"
                ]
