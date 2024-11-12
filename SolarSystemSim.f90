PROGRAM SOLAR_SYSTEM_SIM
    USE CELESTIAL_BODY
    USE LOCAL_SOLAR_SYSTEM
    IMPLICIT NONE

    ! Declaration area
    INTEGER(8) :: COUNTER, I, J, TICKS_END
    INTEGER(8) :: HZ = 2 ! ticks per second, like hertz (I think).
    REAL(KIND=REAL64), DIMENSION(0:2) :: ZERO_ARR = (/0.0, 0.0, 0.0/)

    TYPE(C_BODY), DIMENSION(0:9) :: C_BODY_SYSTEM
    



    ! Program start
    C_BODY_SYSTEM = CREATE_LOCAL_SOLAR_SYSTEM()
    TICKS_END = ((ED_TIME_UNIX - ST_TIME_UNIX) * HZ ) + ST_TIME_UNIX

    DO COUNTER = ST_TIME_UNIX, TICKS_END
        DO I = 0, 8
            DO J = I + 1, 9
                CALL CALC_ACCEL_VECS(C_BODY_SYSTEM(I), C_BODY_SYSTEM(J))
            END DO
        END DO

        DO I = 0, 9
            C_BODY_SYSTEM(I)%V_VEC = C_BODY_SYSTEM(I)%V_VEC + C_BODY_SYSTEM(I)%A_VEC / HZ
            C_BODY_SYSTEM(I)%P_VEC = C_BODY_SYSTEM(I)%P_VEC + C_BODY_SYSTEM(I)%V_VEC / HZ
            C_BODY_SYSTEM(I)%A_VEC = ZERO_ARR
        END DO

        CALL ECLIPSE(C_BODY_SYSTEM, COUNTER, HZ)
    END DO

END PROGRAM SOLAR_SYSTEM_SIM
