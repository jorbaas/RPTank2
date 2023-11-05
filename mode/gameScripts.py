import math



class GameScripts():

    def calculateAngle(self, pos1, pos2):
        angle = math.atan2(pos2[1] - pos1[1], pos2[0] - pos1[0])
        angle = math.degrees(angle)
        return angle % 360

    def hit_angle_calculation(self, bullet, enemy, side):
        print(f'side hit: {side}')
        shot_angle = self.calculateAngle(self.player.tank.rect.center, bullet.rect.center)

        if side == 'front':
            hit_angle =   (shot_angle + (enemy.tank.hull.angle)) % 180
        elif side == 'right':
            hit_angle =   (shot_angle + (enemy.tank.hull.angle + 90)) % 180
        elif side == 'left':
            hit_angle =   (shot_angle + (enemy.tank.hull.angle - 90)) % 180
        elif side == 'rear':
            hit_angle =   (shot_angle + (enemy.tank.hull.angle - 180)) % 180

        if hit_angle - 90 >= 0:
            hit_angle = 90 - (hit_angle - 90)

        print(f'hit angle: {hit_angle}')
        return hit_angle

    def damage_calculation(self, bullet, enemy, side):
        angle = self.hit_angle_calculation(bullet, enemy, side)


        if angle <= bullet.values['ricochet_angle']:
            print('RICOCHET!')
            return

        if side == 'front':
            armor_thickness = enemy.tank.hull.front_armor
        if side in ['left', 'right']:
            armor_thickness = enemy.tank.hull.side_armor
        if side == 'rear':
            armor_thickness = enemy.tank.hull.rear_armor

        # Convert the cutting angle from degrees to radians
        angle_radians = math.radians(90-angle)

        # Calculate the effective thickness
        effective_thickness = armor_thickness / math.cos(angle_radians)
        print(armor_thickness, effective_thickness)

        if bullet.values['max_thickness'] >= effective_thickness:
            damage = bullet.damage - (effective_thickness - armor_thickness + ((armor_thickness/10)**2))
            damage = round(damage, 1)

            enemy.tank.health -= damage
            print(enemy.tank.health)
            self.camera_group.renderDamage(damage, bullet.rect.center)

        else:
            self.camera_group.renderDamage(0, bullet.rect.center)
