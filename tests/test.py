from ball_game.ball import Ball

def test_ball_collision():
    b1 = Ball(1, 1, 3, None, (255, 255, 255))
    b2 = Ball(2, 2, 3, None, (255, 255, 255))

    assert b1.collision(b2)
    