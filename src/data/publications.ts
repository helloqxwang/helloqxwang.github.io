export type PublicationLink = { label: string; href: string; };
export type Author = { name: string; href?: string; isSelf?: boolean; equalContribution?: boolean; };
export type Publication = { title: string; venue: string; year: number; image: string; imageAlt: string; authors: Author[]; links: PublicationLink[]; award?: string; selected?: boolean; };

export const publications: Publication[] = [
  {
    "selected": true,
    "title": "KITE: Decoupling Kinematics and Interaction for Zero-Shot Cross-Embodiment Manipulation",
    "venue": "arXiv preprint arXiv:2606.22113",
    "year": 2026,
    "image": "/images/KITE.png",
    "imageAlt": "KITE: Decoupling Kinematics and Interaction for Zero-Shot Cross-Embodiment Manipulation",
    "authors": [
      {
        "name": "Qianxu Wang",
        "isSelf": true
      },
      {
        "name": "Kuan Fang"
      }
    ],
    "links": [
      {
        "label": "Paper",
        "href": "https://arxiv.org/abs/2606.22113"
      },
      {
        "label": "Website",
        "href": "https://kite-manip.github.io/"
      }
    ]
  },
  {
    "title": "Neural Attention Field: Emerging Point Relevance in 3D Scenes for One-Shot Dexterous Grasping",
    "venue": "Conference on Robot Learning (CoRL)",
    "year": 2024,
    "image": "/images/NeuralAttentionField.png",
    "imageAlt": "Neural Attention Field: Emerging Point Relevance in 3D Scenes for One-Shot Dexterous Grasping",
    "authors": [
      {
        "name": "Qianxu Wang",
        "isSelf": true
      },
      {
        "name": "Congyue Deng",
        "href": "https://cs.stanford.edu/~congyue/"
      },
      {
        "name": "Tyler Lum",
        "href": "https://tylerlum.github.io/"
      },
      {
        "name": "Yuanpei Chen",
        "href": "https://cypypccpy.github.io/"
      },
      {
        "name": "Yaodong Yang",
        "href": "https://www.yangyaodong.com/"
      },
      {
        "name": "Jeannette Bohg",
        "href": "https://web.stanford.edu/~bohg/"
      },
      {
        "name": "Yixin Zhu",
        "href": "https://yzhu.io/"
      },
      {
        "name": "Leonidas Guibas",
        "href": "https://geometry.stanford.edu/member/guibas/"
      }
    ],
    "links": []
  },
  {
    "selected": true,
    "title": "SparseDFF: Sparse-View Feature Distillation for One-Shot Dexterous Manipulation",
    "venue": "International Conference on Learning Representations (ICLR)",
    "year": 2024,
    "image": "/images/SparseDFF.png",
    "imageAlt": "SparseDFF: Sparse-View Feature Distillation for One-Shot Dexterous Manipulation",
    "authors": [
      {
        "name": "Qianxu Wang",
        "isSelf": true
      },
      {
        "name": "Haotong Zhang"
      },
      {
        "name": "Congyue Deng",
        "href": "https://cs.stanford.edu/~congyue/"
      },
      {
        "name": "Yang You",
        "href": "https://qq456cvb.github.io/"
      },
      {
        "name": "Hao Dong",
        "href": "https://zsdonghao.github.io/"
      },
      {
        "name": "Yixin Zhu",
        "href": "https://yzhu.io/"
      },
      {
        "name": "Leonidas Guibas",
        "href": "https://geometry.stanford.edu/member/guibas/"
      }
    ],
    "links": [
      {
        "label": "Paper",
        "href": "https://arxiv.org/abs/2310.16838"
      },
      {
        "label": "Website",
        "href": "https://helloqxwang.github.io/SparseDFF/"
      },
      {
        "label": "Code",
        "href": "https://github.com/helloqxwang/SparseDFF"
      }
    ]
  },
  {
    "title": "Learning a Universal Human Prior for Dexterous Manipulation from Human Preference",
    "venue": "RSS Workshop on Learning Dexterous Manipulation",
    "year": 2023,
    "image": "/images/RLHF.png",
    "imageAlt": "Learning a Universal Human Prior for Dexterous Manipulation from Human Preference",
    "authors": [
      {
        "name": "Zihan Ding",
        "href": "https://quantumiracle.github.io/webpage/"
      },
      {
        "name": "Yuanpei Chen",
        "href": "https://cypypccpy.github.io/"
      },
      {
        "name": "Allen Z. Ren",
        "href": "https://allenzren.github.io/"
      },
      {
        "name": "Shixiang Shane Gu",
        "href": "https://sites.google.com/view/gugurus/home"
      },
      {
        "name": "Qianxu Wang",
        "isSelf": true
      },
      {
        "name": "Hao Dong",
        "href": "https://zsdonghao.github.io/"
      },
      {
        "name": "Chi Jin",
        "href": "https://sites.google.com/view/cjin/home"
      }
    ],
    "links": [
      {
        "label": "Paper",
        "href": "https://arxiv.org/abs/2304.04602"
      },
      {
        "label": "Website",
        "href": "https://sites.google.com/view/openbidexhand"
      }
    ]
  },
  {
    "title": "ImageManip: Image-based Robotic Manipulation with Affordance-Guided Next View Selection",
    "venue": "Arxiv",
    "year": 2023,
    "image": "/images/ImgManip.jpg",
    "imageAlt": "ImageManip: Image-based Robotic Manipulation with Affordance-Guided Next View Selection",
    "authors": [
      {
        "name": "Xiaoqi Li"
      },
      {
        "name": "Yanzi Wang"
      },
      {
        "name": "Yan Shen"
      },
      {
        "name": "Haoran Lu"
      },
      {
        "name": "Qianxu Wang",
        "isSelf": true
      },
      {
        "name": "Iaroslav Ponomarenko"
      },
      {
        "name": "Boshi An"
      },
      {
        "name": "Jiaming Liu"
      },
      {
        "name": "Hao Dong",
        "href": "https://zsdonghao.github.io/"
      }
    ],
    "links": [
      {
        "label": "Paper",
        "href": "https://arxiv.org/abs/2310.09069"
      },
      {
        "label": "Website",
        "href": "https://sites.google.com/view/imagemanip"
      }
    ]
  }
];
