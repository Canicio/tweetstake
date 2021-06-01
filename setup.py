from setuptools import setup, find_packages


setup(name='Tweetstake',
      version='0.0.1',
      description='Application to get tweets of Twitter on specific topics. Specially designed for Big Data collection.',
      author='Carlos Canicio',
      author_email='caniciosoftware@gmail.com',
      url='https://github.com/canicio/tweetstake',
      download_url='https://github.com/canicio/tweetstake/archive/0.0.1.tar.gz',
      maintainer='Carlos Canicio',
      maintainer_email='caniciosoftware@gmail.com',
      license='MIT (Massachusetts Institute of Technology)',
      packages=['tweetstake', 'tweetstake.apps', 'tweetstake.apps.twitter', 'tweetstake.apps.csv', 'tweetstake.apps.common'],
      install_requires=[
            'APScheduler == 3.4.0',
            'certifi == 2017.7.27.1',
            'chardet == 3.0.4',
            'coloredlogs == 7.3',
            'humanfriendly == 4.4.1',
            'idna == 2.5',
            'mongoengine == 0.13.0',
            'oauthlib == 2.0.2',
            'pymongo == 3.5.0',
            'pytz == 2017.2',
            'requests == 2.18.3',
            'requests-oauthlib == 0.8.0',
            'six == 1.10.0',
            'tweepy == 3.5.0',
            'tzlocal == 1.4',
            'urllib3 == 1.26.5',
      ],
      entry_points={
            'console_scripts': [
                  'tweetstake = tweetstake.__main__:App.main'
            ]
      },
      keywords=['tweets', 'twitter', 'bigdata', 'collection'],
      classifiers=[],
      )
