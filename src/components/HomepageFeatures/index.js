import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Generative Learning',
    Svg: require('@site/static/img/undraw_annotation.svg').default,
    description: (
      <>
        These customizable integration agents are easily pieced together by teachers to help their students make connections between ideas.
      </>
    ),
  },
  {
    title: 'Pedagogical Alignment',
    Svg: require('@site/static/img/undraw_start_building.svg').default,
    description: (
      <>
        We build AI solutions informed by this open-source knowledge base, curated by experienced teachers and education scientists / researchers.
      </>
    ),
  },
  {
    title: 'Open Web Evolution',
    Svg: require('@site/static/img/undraw_building_websites.svg').default,
    description: (
      <>
        Turn any website into a community-driven educational resource that carefully guides each student through relevant content.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
