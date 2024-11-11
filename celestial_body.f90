MODULE CELESTIAL_BODY
    USE ISO_FORTRAN_ENV
    IMPLICIT NONE

    REAL(KIND=REAL64), PARAMETER :: G = 6.6743D-11, C = 299792458

    INTEGER, PARAMETER :: ST_TIME_UNIX = 1704067200 ! UNIX time (seconds): Jan 1st, 2024, 00:00:00 GMT
    INTEGER, PARAMETER :: ED_TIME_UNIX = 2020291200 ! UNIX time (seconds): Jan 1st, 2035 (??), 00:00:00 GMT

    INTEGER(8) :: START_TIME = 0, TEMP_TIME = 0, END_TIME = 0
    INTEGER :: ADJUSTED_TIME

    TYPE :: C_BODY
        REAL(KIND=REAL64) :: M ! M is the mass of the celestial object in the SI unit kg.
        REAL(KIND=REAL64) :: R ! R is the radius of the celestial object in the SI unit meters.
        REAL(KIND=REAL64), DIMENSION(0:2) :: P_VEC ! P_VEC is the position vector with its values in meters in 3-D space using the solar barycenter as the origin.
        REAL(KIND=REAL64), DIMENSION(0:2) :: V_VEC ! V_VEC is the velocity vector represents the objects current movement and is measured in m/s.
        REAL(KIND=REAL64), DIMENSION(0:2) :: A_VEC ! A_VEC is the acceleration vector that will be applied when all objects are finished applying forces and is measured in m/s^2.
    END TYPE
    
    CONTAINS

    ! Helper function for cross product
    FUNCTION CROSS_PRODUCT(A, B) RESULT(CROSS_PROD)
        REAL(KIND=REAL64), DIMENSION(0:2), INTENT(IN) :: A, B
        REAL(KIND=REAL64), DIMENSION(0:2) :: CROSS_PROD

        CROSS_PROD(0) = A(1) * B(2) - A(2) * B(1)
        CROSS_PROD(1) = A(2) * B(0) - A(0) * B(2)
        CROSS_PROD(2) = A(0) * B(1) - A(1) * B(0)
    END FUNCTION CROSS_PRODUCT

    ! Calculate and apply the acceleration vectors on two bodies.
    SUBROUTINE CALC_ACCEL_VECS(BODY_ONE, BODY_TWO)
        TYPE(C_BODY), INTENT(INOUT) :: BODY_ONE, BODY_TWO
        REAL(KIND=REAL64), DIMENSION(0:2) :: DISPLACEMENT_VEC, FORCE_VEC
        REAL(KIND=REAL64) :: DISTANCE, CORRECTION_FACTOR

        DISPLACEMENT_VEC = BODY_TWO%P_VEC - BODY_ONE%P_VEC
        DISTANCE = NORM2(DISPLACEMENT_VEC)
        CORRECTION_FACTOR = 1 + ( &
                                    ( &
                                        (.5 * ( NORM2(BODY_ONE%V_VEC)**2 + NORM2(BODY_TWO%V_VEC)**2 ) ) - &
                                        DOT_PRODUCT(BODY_ONE%V_VEC, BODY_TWO%V_VEC) + &
                                        (2 * G * ( BODY_ONE%M + BODY_TWO%M )) / DISTANCE &
                                    ) / C**2 &
                                ) 
        FORCE_VEC = ( DISPLACEMENT_VEC / DISTANCE ) * ( (G * BODY_ONE%M * BODY_TWO%M / DISTANCE**2) * CORRECTION_FACTOR )
        BODY_ONE%A_VEC = BODY_ONE%A_VEC + (FORCE_VEC / BODY_ONE%M)
        BODY_TWO%A_VEC = BODY_TWO%A_VEC + (-1 * FORCE_VEC / BODY_TWO%M)
    END SUBROUTINE CALC_ACCEL_VECS



    ! Checks if an eclipse will occur.
    SUBROUTINE ECLIPSE(SOL_SYS_ARR, CURRENT_TIME, HZ)
        TYPE(C_BODY), DIMENSION(0:9), INTENT(IN) :: SOL_SYS_ARR
        INTEGER, INTENT(IN) :: CURRENT_TIME, HZ
        REAL(KIND=REAL64) :: SUN_TO_EARTH_VEC(3), SUN_TO_EARTH_UNIT_VEC(3)
        REAL(KIND=REAL64) :: SOL_TO_LUNA_VEC(3), PERPENDICULAR_DISTANCE

        ADJUSTED_TIME = ((CURRENT_TIME - ST_TIME_UNIX) / HZ) + ST_TIME_UNIX

        ! Calculate direction vector from the Sun to the Earth
        SUN_TO_EARTH_VEC = SOL_SYS_ARR(3)%P_VEC - SOL_SYS_ARR(0)%P_VEC
        SUN_TO_EARTH_UNIT_VEC = SUN_TO_EARTH_VEC / NORM2(SUN_TO_EARTH_VEC)
        ! Calculate vector from the Sun to the Moon
        SOL_TO_LUNA_VEC = SOL_SYS_ARR(4)%P_VEC - SOL_SYS_ARR(0)%P_VEC
        ! Calculate perpendicular distance
        PERPENDICULAR_DISTANCE = NORM2(CROSS_PRODUCT(SOL_TO_LUNA_VEC, SUN_TO_EARTH_UNIT_VEC))
        ! Check if an eclipse is occurring (alignment condition)
        IF (PERPENDICULAR_DISTANCE <= SOL_SYS_ARR(4)%R + SOL_SYS_ARR(3)%R) THEN
            ! If START_TIME is unset, set it to the beginning of the eclipse
            IF (START_TIME == 0) THEN
                START_TIME = ADJUSTED_TIME
            END IF
            ! Update TEMP_TIME with the current eclipse time
            TEMP_TIME = ADJUSTED_TIME

        ELSE IF (START_TIME /= 0 .AND. TEMP_TIME /= 0) THEN
            ! If eclipse has ended (gap detected), set END_TIME and log the event
            END_TIME = TEMP_TIME
            PRINT "(A, I0, A, I0, A)", "Eclipse from ", START_TIME, " to ", END_TIME, " epoch time."
            PRINT "(A, I0, A)", " Middle: ", (START_TIME + END_TIME) / 2, " epoch time."


            ! Reset START_TIME and TEMP_TIME for the next eclipse
            START_TIME = 0
            TEMP_TIME = 0
        END IF
    END SUBROUTINE ECLIPSE



END MODULE CELESTIAL_BODY