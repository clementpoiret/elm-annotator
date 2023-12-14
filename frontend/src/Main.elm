module Main exposing (..)

import Element exposing (..)
import Element.Background as Background
import Header exposing (..)
import Html exposing (Html)


main : Html Bool
main =
    layout [ width fill, height fill ] <|
        column
            [ width fill
            , height fill
            , centerX
            , centerY
            , Background.image "assets/background.svg"
            ]
            [ header ]
