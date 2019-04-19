from setuptools import setup, find_packages

setup(name='ldhpack',
      version='1.2.0',
      description=(
          '这是一个常用的爬虫开发和深度学习使用的个人开发包，因部分功能比较通用，现将其打包到pip'
      ),
      long_description='For detail please step to https://github.com/ldhsight/pack',
      long_description_content_type="text/markdown",
      author='ldhsights',
      author_email='yfyvan@gmail.com',
      maintainer='Yvan L',
      maintainer_email='yvan@gmail.com',
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      url='https://github.com/ldhsight/pack',
      classifiers=[
          "Environment :: Web Environment",
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "Topic :: Text Processing :: Indexing",
          "Topic :: Utilities",
          "Topic :: Internet",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Programming Language :: Python",
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7'
      ],
      install_requires=[
          'pymssql',
          'pymysql',
          'pymongo',
          'py2neo',
          'pdfplumber',
          'concurrent_log_handler',
          'pillow',
          'numpy',
          'scipy',
          'matplotlib',
          'redis',
          'pandas',
          'pydot',
          'opencv-python',
          'jieba',
          'pyspark'
      ])
