from django.contrib.auth import models

class DiscordUserOAuth2Manager(models.UserManager):

    def create_discord_user(self, user, user_id):
        discord_tag = f"{user['username']}#{user['discriminator']}"
        new_user = self.create(
            id=user['id'],
            discord_tag=discord_tag,
            avatar=user['avatar'],
            email=user['email'],
            public_flags=user['public_flags'],
            flags=user['flags'],
            locale=user['locale'],
            mfa_enabled=user['mfa_enabled'],
            user=user_id
        )
        return new_user